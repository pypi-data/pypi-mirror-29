from settings import settings
from ucesb import UcesbDriver
from state import State
import logging


class Relay:

    def __init__(self, *args, **kwargs):
        hostname = kwargs.get("hostname")
        self.cmd = [settings['relay']['unpacker'],
                    '--stream={}'.format(hostname),
                    '--quiet']
        self.cmd.extend(settings['relay']['flags'])

        self.ucesb = None
        self.__stop = None
        self.backend_log = logging.getLogger("backend")
        self.backend_log.info("Created Relay")

    def start(self):
        self.backend_log.info("Starting relay")
        self.__stop = False
        self.ucesb = UcesbDriver(self.cmd, settings['relay']['monitor'], logging.getLogger("relay_ucesb"))
        self.backend_log.info("Starting relay - done")

    def stop(self):
        self.backend_log.info("Stopping relay")
        self.__stop = True
        if self.ucesb is not None:
            self.ucesb.stop()
        self.backend_log.info("Stopping relay - done")

    def is_running(self):
        return self.ucesb.is_running() if self.ucesb is not None else False

    def progress(self):                
        return self.ucesb.progress() if self.ucesb is not None else (0, 0)

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


class MockRelay:
    def __init__(self, **_):
        self.running = None
        self.events = 0
        self.error = 0
        self.backend_log = logging.getLogger("backend")
        self.backend_log.info("Created MockRelay")

    def stop(self):
        self.backend_log.info("Stopping MockRelay")
        self.running = False
        self.backend_log.info("Stopping MockRelay - done")

    def start(self):
        self.backend_log.info("Starting MockRelay")
        self.running = True
        self.backend_log.info("Starting MockRelay - done")

    def is_running(self):
        self.events += 1000
        if self.events % 50000:
            self.error += 1

        return self.running

    def progress(self):
        return self.events, self.error

    def state(self):
        if self.running is None:
            return State.STANDBY
        elif self.running:
            self.events += 1000
            if self.events % 50000 == 0:
                self.error += 1
            return State.RUNNING
        else:
            return State.STOPPED
