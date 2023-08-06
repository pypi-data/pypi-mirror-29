from threading import Thread
from ptyprocess import PtyProcess
from subprocess import Popen, PIPE
from util import get_open_port, DEV_NULL
import time
import json


class UcesbDriver:
    def __init__(self, flags, monitor, log):
        self.monitor = monitor
        self.log = log
        self.monitor_port = get_open_port()

        flags_copy = list(flags)
        flags_copy.extend(['--monitor=%d' % self.monitor_port])
        print flags_copy
        self.process = PtyProcess.spawn(flags_copy)

        self.events = 0
        self.multi_events = 0
        self.errors = 0

        # Launch monitor thread
        monitor_thread = Thread(target=self.__monitor)
        monitor_thread.daemon = True
        monitor_thread.start()

        output_thread = Thread(target=self.__read_output)
        output_thread.daemon = True
        output_thread.start()

    def stop(self):
        self.process.sendintr()

        for i in range(0, 25):
            time.sleep(0.1)
            if not self.is_running(): return

        self.process.sendintr()
        self.process.sendintr()

        for i in range(0, 5):
            time.sleep(0.1)
            if not self.is_running(): return

        self.process.terminate()

    def read(self):
        return self.process.read()

    def __monitor(self):
        p = Popen([self.monitor, "--dump=compact_json", "localhost:{}".format(self.monitor_port)],
                  stdout=PIPE, stderr=DEV_NULL)

        time.sleep(1)
        for line in iter(p.stdout.readline, b''):
            status = json.loads(line)

            self.errors = status['errors']
            self.multi_events = status['multi_events']
            self.events = status['events']

    def __read_output(self):
        try:
            while 1:
                r = self.read()
                if r is None: continue
                lines = r.splitlines()
                for line in lines:
                    self.log.critical(line)

                time.sleep(1)
        except EOFError:
            pass

    def is_running(self):
        return self.process.isalive()

    def progress(self):
        return self.multi_events, self.errors
