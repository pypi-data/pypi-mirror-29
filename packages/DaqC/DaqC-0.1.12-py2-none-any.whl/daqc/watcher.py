import time
import threading
import logging

from state import State

BAD_STATES = [State.CRASHED, State.STANDBY]
ALIVE_STATES = [State.RUNNING, State.WAITING]
RETRY_SEQ = [1, 1, 1, 10, 20, 30, 40, 50, 60, 120, 180, 240, 300]


def keep_forever(seq):
    for k in seq:
        yield k
    while 1:
        yield seq[-1]


class Puppy:
    def __init__(self, name, subject, depends_on=None):
        self.name = name
        self._start = subject.start
        self._running = subject.is_running
        self._subject = subject
        self.should_stop = True
        self.status = State.STOPPED
        self.depends_on = depends_on
        self.log = logging.getLogger("backend")
        self.thread = None

    def is_dependency_alive(self):
        if self.depends_on is None:
            return True
        else:
            return self.depends_on.status in ALIVE_STATES

    def run(self):
        while 1:
            if self.should_stop:
                return

            self.status = self._subject.state()

            if self.is_dependency_alive() and self.status in BAD_STATES:
                for n in keep_forever(RETRY_SEQ):
                    if not self.is_dependency_alive():
                        break
                    self.log.info("Attempting restart of {}".format(self.name))
                    self._start()
                    self.status = self._subject.state()
                    if self.status not in BAD_STATES:
                        self.log.info("{} revived".format(self.name))
                        break
                    else:
                        self.log.warn("{} revive failed. Will try again in {} sec.".format(self.name, n))
                        start = time.time()
                        while time.time() - start < n:
                            time.sleep(1)
                            if self.should_stop:
                                return
            time.sleep(1)

    def start(self):
        self.should_stop = False
        t = threading.Thread(target=self.run)
        t.daemon = True
        t.start()
        self.thread = t

    def stop(self):
        if self.thread is not None:
            self.should_stop = True
            self.thread.join()


class WatchDog:
    def __init__(self):
        self._subjects = {}

    def add(self, name, subject, depends):
        self._subjects[name] = Puppy(name, subject, self._subjects.get(depends))

    def status(self):
        status = {}
        for name, subject in self._subjects.iteritems():
            status.update({name: {
                "message": subject.status,
                "status": subject.status.lower()
            }})
        return status

    def start(self):
        for _, p in self._subjects.iteritems():
            p.start()

    def stop(self):
        for _, p in self._subjects.iteritems():
            p.stop()
