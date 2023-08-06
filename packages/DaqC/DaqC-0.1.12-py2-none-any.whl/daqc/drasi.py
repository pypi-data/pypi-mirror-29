import logging
import util
from settings import settings
import re
import threading
import time
from state import State
import subprocess
import shlex
import os

STATES = {
    State.RUNNING: ["run", "inspill", "offspill"],
    State.STOPPED: ["stopped"],
    State.STARTING: ["ReInit"],
    State.CRASHED: ["NoDiagns", "Local", "Net", "EB_ID", "Mism", "ECmism", "ECdsync", "DataCon"],
    State.WAITING: ["WtAbort", "WtTerm", "WtConn", "WtEBClr", "WtIdent", "WtTest",
        "WtRun", "WaitNet", "Readout", "BufSpace", "DeadTime", "WtMaster", "WtSlave"]
}

STATE_MAP = {k: s for s, l in STATES.iteritems() for k in l}


class Drasi:
    def __init__(self, *args, **kwargs):

        self.SSH_TARGET, self.PASS = kwargs.get("ssh_target")
        self.DIR = kwargs.get("directory")
        self.command = kwargs.get("command")
        self.user = kwargs.get("user")
        self.log_file = kwargs.get("log_file")

        hostname = settings['drasi']['hostname']
        lwrocmon = settings['drasi']['lwrocmon']

        self.start_up_timeout = settings['drasi']['start_up_timeout']

        self.start_cmd = 'ssh {}@{} "cd {} && {}"'.format(self.user, self.SSH_TARGET, 
                                                          self.DIR, self.command)
        self.mon_cmd = '{} {} --rate --count=2'.format(lwrocmon, hostname)

        self.log_cmd = '{} {} --log="{}"'.format(lwrocmon, hostname, self.log_file)

        FNULL = open(os.devnull, 'w')
        subprocess.Popen(shlex.split(self.log_cmd), close_fds=True, stdout=FNULL, stderr=FNULL)

        self.log = logging.getLogger("backend")

        self.start_process = None
      
        self._running = None
        self._stopped = None

        self._rate_events = 0
        self._rate_data = 0
        self._rate_state = State.STANDBY
        self._message = "Standby"

        self._has_parse_error = False

        self.monitor()
        
        t = threading.Thread(target=self.do_watch)
        t.daemon = True
        t.start()

    def monitor(self):
        
        if self._rate_state == State.STANDBY:
            return
        
        p = util.ReturningCommand(self.mon_cmd).run().get()
        if "Connection refused" in p[1]:
            self._running = False
            self._rate_events = self._rate_data = ""
            self._rate_state = State.CRASHED
            self._message = "No conn"
        else:
            self._running = True
            s = p[0].split("\n")
            m = re.search("^\s*(\w*)\s*[0-9a-z\-:]*\s*(\d*)\s*(\d*|\-)\s*(\d+\.?\d*|\-)[kM]?\s*(\d+\.?\d*)\%\s*(\d+.?\d*)[kM]?", s[4])
            if m is not None:
                self._rate_state = STATE_MAP[str(m.group(1))]
                self._rate_events = int(m.group(3)) if m.group(3) != "-" else 0
                self._rate_data = float(m.group(4)) if m.group(4) != "-" else 0.0
                self._has_parse_error = False
                self._message = "Running" if self._rate_state is State.RUNNING else str(m.group(1))
            else:
                self._rate_state = State.RUNNING
                self._rate_events = self._rate_data = "Parse error"
                self._message = "Running"

                if not self._has_parse_error:
                    self.log.error("Parse error in lwrocmon output. Can not understand '{}'".format(s[4]))
                    self._has_parse_error = True

    def do_watch(self):
        while 1:
            try:
                self.monitor()        
            except:
                pass

    def is_running(self):
        return self._running

    def start(self):
        self._rate_state = State.STARTING
        self._stopped = False
        if self._running is None:
            self.monitor()
        if self._running:
            self.log.info("Drasi already running!")
        else:
            self.log.info("Starting Drasi")
            self.start_process = util.ReturningCommand(self.start_cmd)
            self.start_process.run()
            start_time = time.time()
            while not self.is_running():
                t = time.time() - start_time
                self.log.debug("Waiting for drasi {}".format(t))
                if t > self.start_up_timeout:
                    self.log.warning("Drasi startup timed out (60s)")
                    return
                time.sleep(0.1)

            self.log.info("Started Drasi")

    def stop(self):
        self.log.info("Stopping Drasi")
        self.start_process.terminate()
        self.start_process = None
        self._stopped = True
        self.log.info("Stopped Drasi")

    def status(self):
        return {'bl_r_events': self._rate_events,
                'bl_r_kbyte': self._rate_data,
                'message': self._message}

    def state(self):
        return self._rate_state

    def get_name(self):
        return "DRASI"

    def get_message(self):
        return self._message

class MockDrasi:
    def __init__(self, **_):
        self.running = None
        self.backend_log = logging.getLogger("backend")
        self.backend_log.info("Created MockDrasi")

    def stop(self):
        self.backend_log.info("Stopping MockDrasi")
        self.running = False
        self.backend_log.info("Stopping MockDrasi - done")

    def start(self):
        self.backend_log.info("Starting MockDrasi")
        self.running = True
        self.backend_log.info("Starting MockDrasi - done")

    def is_running(self):
        return self.running

    @staticmethod
    def status():
        interesting = ['bh_acqui_started', 'bh_acqui_running', 'bl_n_events',
                       'bl_n_kbyte', 'bl_n_strserv_kbytes', 'bl_r_events',
                       'bl_r_kbyte', 'bl_r_strserv_kbytes', 'bl_pipe_size_KB',
                       'bl_pipe_size_KB', 'bl_pipe_filled_KB']

        result = {}
        for i in interesting:
            result[i] = 0

        return result

    def state(self):
        if self.running is None:
            return State.STANDBY
        elif self.running:
            return State.RUNNING
        else:
            return State.STOPPED

    def get_name(self):
        return "MockDRASI"

    def get_message(self):
        return self.state()
