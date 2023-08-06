import util
import json
import time
import threading
import logging
from state import State


class Mesytec:
    def __init__(self, **kwargs):
        if not kwargs.get("command"):
            raise ValueError("No Mesytec command")

        if not kwargs.get("file"):
            raise ValueError("No Mesytec file")

        self.log = logging.getLogger("backend")
        self.command = kwargs["command"]
        self.settings_file = kwargs["file"]
        self.sleep = int(kwargs.get("sleep", 60))
        self.good = None
        self._stop = None
        self.thread = None
        self._last_check = None

    def check(self):
        stdout, _ = util.ReturningCommand(self.command).run().get()
        current = json.loads(stdout)
        self._last_check = util.build_timestamp()

        with open(self.settings_file) as f:
            c = f.read()

            reference = json.loads(c)
            reference.pop('comment', None)
            reference.pop('time', None)

            return current == reference

    def monitor(self):
        while True:
            self.good = self.check()

            for _ in xrange(self.sleep):
                if self._stop:
                    return

                time.sleep(1)

    def last_check(self):
        return self._last_check

    def is_running(self):
        return not self._stop

    def start(self):
        self.log.info("Starting Mesytec checker")
        self._stop = False
        
        t = threading.Thread(target=self.monitor)
        t.daemon = True
        t.start()
        self.thread = t

        self.log.info("Started Mesytec checker")

    def stop(self):
        self.log.info("Stopping Mesytec checker")
        self._stop = True
        self.log.info("Stopped Mesytec checker")

    def status(self):
        if self.good is None:
            return "Unknown"
        elif self.good:
            return "Match"
        else:
            return "Changed!"

    def state(self):
        if self._stop is None:
            return State.STANDBY
        elif self._stop:
            return State.STOPPED
        elif self.thread and not self.thread.isAlive():
            return State.CRASHED
        elif self.good is None:
            return State.STARTING
        elif self.good:
            return State.RUNNING
        else:
            return State.ERROR


class MockMesytec:
    def __init__(self, **_):
        self.running = None
        self.backend_log = logging.getLogger("backend")
        self.backend_log.info("Created MockMesytec")

    def stop(self):
        self.backend_log.info("Stopping MockMesytec")
        self.running = False
        self.backend_log.info("Stopping MockMesytec - done")

    def start(self):
        self.backend_log.info("Starting MockMesytec")
        self.running = True
        self.backend_log.info("Starting MockMesytec - done")

    def status(self):
        if self.running is None:
            return "Unknown"
        elif self.running:
            return "Configured"
        else:
            return "Configuration changed!"

    def is_running(self):
        return self.running

    def last_check(self):
        return util.build_timestamp()

    def state(self):
        if self.running is None:
            return State.STANDBY
        elif self.running:
            return State.RUNNING
        else:
            return State.STOPPED
