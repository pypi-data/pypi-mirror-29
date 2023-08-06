import sys
import os
import logging
from rest import RestApi
from watcher import WatchDog
from settings import settings
from util import CustomRotatingFileHandler


def parse_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--settings', help='Path to settings file', required=True)
    parser.add_argument('--lib', type=str, default="MBS", help='Which readout library to use. Choose between MBS and drasi', required=True)
    parser.add_argument('--secret', help='File with REST secret', default=".daqc-secret")
    parser.add_argument('--mock', action='store_true', default=False, help='Enable mocking')
    parser.add_argument('--reload', action='store_true', default=False, help='Enable reloader')
    parser.add_argument('--port', type=int, default=8080, help='Port to listen on')
    parser.add_argument('--interface', type=str, default="0.0.0.0", help='Interface to listen on')
    parser.add_argument('--log', type=str, default='.', help='Path to the main log. If it is a directory, the file is automatically called <your path>/daqc.log')
    parser.add_argument('--log-size', type=float, default=5, help='Size of the logfile in MB before it is rotated into old_logs')

    return parser.parse_args()


def main():
    watchdog = None
    go4 = None
    relay = None
    file_taker = None
    sync = None

    args = parse_args()
    settings.read(args.settings)
    mocking = args.mock

    try:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        backend_log = logging.getLogger('backend')
        backend_log.addHandler(stdout_handler)
        backend_log.setLevel(logging.DEBUG)

        if mocking:
            from mbs import MockMBS as MBS
            from drasi import MockDrasi as Drasi
            from relay import MockRelay as Relay
            from file_taker import MockFileTaker as FileTaker
            from vme import MockVME as VME
            from sync import MockSync as Sync
            from go4 import MockGo4WebServer as Go4WebServer
            from mesytec import MockMesytec as Mesytec
            from trigger import MockTrigger as Trigger
            from user import TestUserDatabase
            from rundb import MockRunDb as RunDb
            users = TestUserDatabase()

            run_handler = logging.FileHandler("mock_runs.log")
        else:
            from mbs import MBS
            from drasi import Drasi
            from relay import Relay
            from file_taker import FileTaker
            from vme import VME
            from sync import Sync
            from go4 import Go4WebServer
            from mesytec import Mesytec
            from trigger import Trigger
            from user import JsonUserDatabase
            from rundb import RunDb
            users = JsonUserDatabase(settings['users']['path'])

            if users.is_empty():
                import getpass
                print("No users - please register one")
                uname = raw_input("Username: ")
                passwd = getpass.getpass("Password: ")
                users.add(uname, passwd)



            run_handler = logging.FileHandler(settings['logs']['runs_log'])

        log_path = args.log
        if os.path.isdir(log_path):
            log_path = os.path.join(log_path, 'daqc.log')
        backend_handler = logging.FileHandler(log_path)
        backend_handler.setLevel(logging.INFO)
        backend_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))

        logging.getLogger('backend').addHandler(backend_handler)
        logging.getLogger('backend').addHandler(CustomRotatingFileHandler("daqc.log", int(args.log_size*1e6), "old_logs"))

        run_handler.setLevel(logging.INFO)
        logging.getLogger('files').addHandler(run_handler)
        logging.getLogger('files').setLevel(logging.INFO)

        readout_lib = args.lib.lower()
        if readout_lib not in ("mbs", "drasi"):
            raise ValueError("Unknown readout lib {}. Only supports MBS/drasi".format(args.lib))



        # Readout lib (mbs/drasi)
        remote = settings[readout_lib]['hostname']
        f_user_dir = settings[readout_lib]['f_user_dir']
        user = settings[readout_lib]['user']

        if args.lib.lower() == 'mbs':
            vme_lib = MBS(ssh_target=(remote, None), directory=f_user_dir, user=user)
        elif args.lib.lower() == 'drasi':
            vme_lib = Drasi(ssh_target=(remote, None), directory=f_user_dir,
                        command=settings['drasi']['command'], log_file=settings['drasi']['log_file'],
                        user=user)

        # Ping command
        vme = VME(remote)

        # Relay
        relay = Relay(hostname=remote)

        # GO4
        go4 = Go4WebServer(settings['go4']['lib'], settings['go4']['port'],
                           settings['go4']['ucesb_args'], settings['go4'].get('extra_args', ''))
        if not settings['go4'].get('enabled', True):
            go4.stop()

        sync = Sync(settings['file_taking']['data_dir'], settings['sync']['destinations'],
                    settings['sync']['ripe_age'], settings['sync']['active_wait'])

        file_taker = FileTaker(remote)

        mesytec = Mesytec(command=settings['mesytec']['command'], file=settings['mesytec']['file'],
                          sleep=settings.get('mesytec').get('sleep'))
        if not settings['mesytec'].get('enabled', True):
            mesytec.stop()

        trigger = Trigger(remote=remote, port=settings['trigger']['port'],
                          name_cmd=settings['trigger']['name_cmd'],
                          trloctrl=settings['trigger']['trloctrl'],
                          vulom_address=settings['trigger']['vulom_address'])

        rundb = RunDb(url=settings["run_db"]["url"],
                      api_version=settings["run_db"]["api_version"],
                      api_key=settings["run_db"]["api_key"])

        watchdog = WatchDog()
        watchdog.add('vme', vme, None)
        watchdog.add('vme_lib', vme_lib, 'vme')
        watchdog.add('relay', relay, 'vme_lib')
        watchdog.add('go4', go4, 'relay')
        watchdog.add('sync', sync, None)
        watchdog.add('mesytec', mesytec, None)
        watchdog.start()

        rest = RestApi(vme=vme, vme_lib=vme_lib, relay=relay, go4=go4, sync=sync,
                       file_taker=file_taker, watchdog=watchdog, users=users,
                       mesytec=mesytec, trigger=trigger, rundb=rundb,
                       secret=args.secret)

        rest.app.run(host=args.interface, port=args.port, debug=True, use_reloader=args.reload)
    except Exception, err:
        import traceback
        traceback.print_exc()

    finally:
        def guarded_stop(name, obj, f_name):
            def _print(trace):
                if backend_log is not None:
                    backend_log.info(trace)
                else:
                    print trace

            try:
                _print("GUARD: Stopping %s" % name)
                if obj is not None:
                    f = getattr(obj, f_name)
                    f()
                _print("GUARD: Stopping %s - done" % name)
            except:
                import traceback
                _print("GUARD: Stopping %s - failed" % name)
                traceback.print_exc()

        guarded_stop("Watchdog", watchdog, 'stop')
        guarded_stop("GO4", go4, 'stop')
        guarded_stop("Relay", relay, 'stop')
        guarded_stop("File", file_taker, 'stop_and_wait')
        guarded_stop("Sync", sync, 'stop')
        # guarded_stop("Readout", r.mbs_stop)

if __name__ == '__main__':
    main()