import subprocess
import logging
import util
from state import State
import threading
import time

class VME:
    def __init__(self, hostname):
        self.hostname = hostname
        self.backend_log = logging.getLogger("backend")
        self.backend_log.info("Created MVE")

        self.__is_running = None
        t = threading.Thread(target=self.__monitor)
        t.daemon = True
        t.start()

    def start(self):
        self.backend_log.info("VME can not be started!")

    def stop(self):
        self.backend_log.info("VME can not be stopped!")

    def is_running(self):
        return self.__is_running

    def status(self):
        if not self.is_running():
            return "Offline"
        else:
            return "Online"

    def state(self):
        if self.is_running():
            return State.RUNNING
        else:
            return State.CRASHED

    def __monitor(self):
        while True:
            self.__is_running = self.__ping()
            time.sleep(1)

    def __ping(self):
        ret = subprocess.call(["ping", "-c", "1","-W","1", self.hostname],
                              stdout=util.DEV_NULL, stderr=util.DEV_NULL)
        if ret != 0:
            self.backend_log.error("Ping response from VME was '{}'".format(ret))
        return ret == 0

    def get_name(self):
        return self.hostname


class MockVME:
    def __init__(self, *_):
        self.running = None
        self.backend_log = logging.getLogger("backend")
        self.backend_log.info("Created MockVME")

    def start(self):
        self.backend_log.info("Starting MockVME")
        self.running = True
        self.backend_log.info("Starting MockVME - done")

    def stop(self):
        self.backend_log.info("Stopping MockVME")
        self.running = False
        self.backend_log.info("Stopping MockVME - done")

    def is_running(self):
        return self.running

    def status(self):
        if not self.is_running():
            return "Offline"
        else:
            return "Online"

    def state(self):
        if self.running is None:
            return State.STANDBY
        elif self.running:
            return State.RUNNING
        else:
            return State.STOPPED

    def get_name(self):
        return "MockVME"
