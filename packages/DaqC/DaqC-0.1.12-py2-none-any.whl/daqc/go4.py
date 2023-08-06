import logging
import socket
import subprocess
import time
import shlex
from threading import Thread

from state import State


class Go4WebServer:
    def __init__(self, lib, port, args, extra):
        args += " --quiet"
        self.command = "go4analysis -lib {} -http {} {} -args {}".format(lib, port, extra, args)
        self.p = None
        self.__stop = None
        self.start_time = time.time()
        self.port = port
        self.backend_log = logging.getLogger("backend")
        self.log = logging.getLogger("go4")
        self.__output_thread = None
        
    def is_running(self):
        s = socket.socket()
        try:
            s.connect(("localhost", self.port))
            ret = True
        except Exception as e:
            # self.backend_log.warning("go4 connect failed due to %s" % e)
            ret = False
        finally:
            s.close()
        return ret

    def _process_alive(self):
        if self.p is None:
            return False
        else:
            return self.p.poll() is not None

    def __read_output(self):
        try:
            for line in iter(self.p.stdout.readline, b''):                
                if line is not None:
                    self.log.critical(line)
                if self.p is None:
                    break
        except EOFError:
            pass

    def __start_log_output_thread(self):
        output_thread = Thread(target=self.__read_output)
        output_thread.daemon = True
        output_thread.start()
        print(self.__output_thread)
        self.__output_thread = output_thread

    def stop(self):
        self.backend_log.info("Stopping go4")
        self.__stop = True
        
        if self.p is not None:
            self.p.kill()
            self.p = None
        if self.__output_thread is not None:
            self.__output_thread.join(5)
        self.backend_log.info("Stopping go4 - done")

    def start(self):
        self.backend_log.info("Starting go4")
        self.__stop = False

        self.start_time = time.time()
        self.p = subprocess.Popen(shlex.split(self.command), stderr=subprocess.STDOUT,
                                            stdout=subprocess.PIPE)

        self.__start_log_output_thread()

        self.backend_log.info("Starting go4 - done")

    def state(self):
        if self.__stop:
            if self.is_running():
                return State.STOPPING
            else:
                return State.STOPPED

        elif self.__stop is None:
            return State.STANDBY

        else:
            if self.is_running():
                return State.RUNNING
            elif time.time() - self.start_time < 10:
                return State.STARTING
            else:
                return State.CRASHED


class MockGo4WebServer:
    def __init__(self, *_):
        self.backend_log = logging.getLogger("backend")
        self.running = None
        self.backend_log.info("Created MockGo4WebServer")

    def stop(self):
        self.backend_log.info("Stopping Mock go4")
        self.running = False
        self.backend_log.info("Stopping Mock go4 - done")

    def start(self):
        self.backend_log.info("Starting Mock go4")
        self.running = True
        self.backend_log.info("Starting Mock go4 - done")

    def is_running(self):
        return self.running

    def state(self):
        if self.running is None:
            return State.STANDBY
        elif self.running:
            return State.RUNNING
        else:
            return State.STOPPED
