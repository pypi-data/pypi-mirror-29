from state import State
from util import read_file, write_file, RunFile, ReturningCommand, build_timestamp, get_nr_files, remove_write_permissions
from ucesb import UcesbDriver
from settings import settings
import logging
import threading
import time
import random


class LogBuilder:
    def __init__(self):
        input = settings['file_logging']['commands']
        print input
        self.commands = []
        for entry in input:
            name = entry['name']
            cmd = entry['cmd']
            self.commands.append((name, cmd, ReturningCommand(cmd).run()))

        print self.commands
        self.start = build_timestamp()

    def build(self):
        log = "Current time is: %s\n" % self.start

        for name, cmd, res in self.commands:
            log += "--------------- {} START ---------------\n".format(name)
            log += "%s\n%s\n" % res.get()
            log += "--------------- {} DONE  --------------\n".format(name)

        return log


class SingleFileTaker:
    def __init__(self, data_dir, unpacker, remote, global_log, file_size):
        
        self.file = RunFile()
        self.data_dir = data_dir

        self.filename = "%s/%s_000.lmd.gz" % (self.data_dir, self.file.get_run_nr())
        self.building_log = False
        
        cmd = [
            unpacker,
               "trans://{}".format(remote),
               "--output=clevel=1,log={},newnum,wp,bufsize=32ki,size={},{}"
               		.format(global_log, file_size, self.filename),
               "--allow-errors",
               "--colour=no",
               "--quiet"
        ]
        self.pre_log = LogBuilder()
        self.ucesb = UcesbDriver(cmd, settings['file_taking']['monitor'], logging.getLogger("file_ucesb"))
        self.log = logging.getLogger("backend")
        self.filelog = logging.getLogger("files")
        self.starttime = self.file.set_start()
        
        self.log.info("Starting file {} @ {}".format(self.filename, self.starttime))
        self._stop_requested = False

    def is_running(self):
        return self.ucesb.is_running() or self.building_log

    def is_stopping(self):
        return self.building_log

    def progress(self):                
        return self.ucesb.progress()

    def __build_log(self):
        f = self.file
        print "Building pre log"
        pre = self.pre_log.build()
        print "Building pre log - done"
        
        print "Building post log"
        post = LogBuilder().build()
        print "Building post log - done"
        self.building_log = False

        log_file = "%s/%s.log" % (self.data_dir, self.get_filename())
        
        log = "Log file for run: %d\n" % self.file.get_run_nr();
        log += "***************************************************\n";
        log += "---------------------- PRELOG ---------------------\n";
        log += "***************************************************\n";
        log += pre
        log += "\n"
        log += "****************************************************\n";
        log += "---------------------- POSTLOG ---------------------\n";
        log += "****************************************************\n";
        log += post
        log += "\n"
        log += "Ending run @ %s" % self.stoptime
        
        write_file(log_file, log)
        remove_write_permissions(log_file)
        f.set_log(log)

    def get_filename(self):
        return self.file.get_run_nr()

    def update_info(self, info):
        self.file.set_info(info)

    def get_info(self):
        return self.file.get_info()

    def stop(self):
        if self._stop_requested:
            return None

        self._stop_requested = True

        self.ucesb.stop()
        self.stoptime = self.file.set_stop()
        self.file.set_info({'n_files': get_nr_files("{}/{}_*.lmd.gz".format(self.data_dir, self.file.get_run_nr()))})

        self.building_log = True
        t = threading.Thread(target=self.__build_log)
        t.start()
        self.log.info("Ending file {} @ {}".format(self.filename, self.stoptime))
        return self.file


class FileTaker:
    def __init__(self, remote):
        self.filer = None

        self.data_dir = settings['file_taking']['data_dir']
        self.unpacker = settings['file_taking']['unpacker']
        self.remote = remote
        self.run_log = settings['file_taking']['run_log']
        self.log = logging.getLogger("files")

        self.__stop = None

        self.backend_log = logging.getLogger("backend")
        self.backend_log.info("Created FileTaker")

    def start(self, file_size):
        self.backend_log.info("Starting FileTaker")
        self.__stop = False
        self.filer = SingleFileTaker(self.data_dir, self.unpacker,
                                     self.remote, self.run_log, file_size)
        self.backend_log.info("Starting FileTaker - done")

    def prefix(self):
        if self.filer is None:
            return ""
        else:
            return self.filer.get_filename()

    def update_info(self, info):
        self.filer.update_info(info)

    def get_info(self):
        if self.filer:
            return self.filer.get_info()
        else:
            raise ValueError("FileTaker has no associated filer!")

    def stop(self):
        self.backend_log.info("Stopping FileTaker")
        self.__stop = True
        if self.filer is None: return None

        f = self.filer.stop()
        if f is not None:
            self.log.info(f.get_yaml())
        self.backend_log.info("Stopping FileTaker - done")
        return f

    def stop_and_wait(self):
        self.backend_log.info("Stopping and waiting FileTaker")
        if self.filer is None: return

        self.stop()
        while self.is_stopping():
            time.sleep(0.1)

        self.backend_log.info("Stopping and waiting FileTaker - done")

    def starttime(self):
        if self.filer is None:
            return ""
        return self.filer.starttime

    def is_running(self):
        if self.filer is None:
            return False
        return self.filer.is_running()

    def progress(self):
        if self.filer is None:
            return 0, 0
        return self.filer.progress()

    def is_stopping(self):
        if self.filer is None:
            return False
        else:
            return self.filer.is_stopping()

    def state(self):
        if self.__stop:
            if self.is_running():
                return State.STOPPING
            else:
                return State.STOPPED
        else:
            if self.is_running():
                return State.RUNNING
            else:
                return State.CRASHED


class MockFileTaker:
    def __init__(self, remote):
        self.info = None
        self.running = False
        self.timestamp = None
        self.events = 0
        self.error = 0
        self.backend_log = logging.getLogger("backend")
        self.backend_log.info("Created MockFileTaker")
        self.file = None
        self.__stopping = False

    def start(self, file_size):
        self.backend_log.info("Started MockFileTaker")
        self.running = True
        self.timestamp = build_timestamp()
        self.file = RunFile()
        self.file.set_start()
        self.backend_log.info("Started MockFileTaker - done")

    def prefix(self):
        return "Mock"

    def update_info(self, info):
        self.file.set_info(info)

    def get_info(self):
        return self.file.get_info()

    def get_filename(self):
        return self.file.get_run_nr()

    def __build_log(self):
        self.__stopping = True
        time.sleep(4)
        self.file.set_log("Mock log for run {}".format(self.file.get_run_nr()))
        self.__stopping = False

    def stop(self):
        self.backend_log.info("Stopping MockFileTaker")
        self.running = False
        self.file.set_stop()
        self.file.set_info({'n_files': random.randint(1, 100)})
        t = threading.Thread(target=self.__build_log)
        t.start()
        self.backend_log.info("Stopping MockFileTaker - done")
        return self.file

    def stop_and_wait(self):
        self.backend_log.info("Stopping and waiting MockFileTaker")
        self.stop()
        self.backend_log.info("Stopping and waiting MockFileTaker - done")

    def starttime(self):
        if self.timestamp is None:
            return ""
        return self.timestamp

    def is_running(self):
        self.events += 1000
        if self.events % 50000:
            self.error += 1

        return self.running

    def progress(self):
        return self.events, self.error

    def is_stopping(self):
        return self.__stopping

    def state(self):
        if self.running is None:
            return State.STANDBY
        elif self.running:
            return State.RUNNING
        else:
            return State.STOPPED
