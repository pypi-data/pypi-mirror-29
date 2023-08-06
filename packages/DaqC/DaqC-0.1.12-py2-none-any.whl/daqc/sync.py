import time
import threading
import subprocess
from settings import settings
import logging
import collections
import util
import os
from state import State

# Watchdog lib: https://github.com/gorakhargosh/watchdog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCHED = {}
LOG = logging.getLogger("backend")

class Sync:
    def __init__(self, directory, targets, ripe_age, active_wait):
        self.backend_log = logging.getLogger("backend")
        self.backend_log.info("Creating Sync")

        if directory[-1] != os.sep:
            directory += os.sep

        self.directory = directory
        self.targets = targets
        self.ripe_age = ripe_age
        self.active_wait = active_wait

        self.should_stop = False
        self.stopped = False
        self.__sync_thread = None
        self.observer = None
        self.last = collections.deque(maxlen=settings['logs']['n_sync_log'])
        for s in reversed(util.get_last_synced(settings['logs']['n_sync_log'])):
            self.last.append(s)
        self.backend_log.info("Creating Sync - done")

    def start(self):
        self.backend_log.info("Starting Sync")
        self.should_stop = False
        self.stopped = False

        LOG.info("Started sync for {}".format(self.directory))

        event_handler = Handler()
        self.observer = Observer()
        self.observer.schedule(event_handler, self.directory, recursive=False)
        self.observer.start()
        
        def __syncer():
            while 1:                
                marked = []

                for f,t in WATCHED.iteritems():
                    d = time.time()-t
                    if self.should_stop or d > self.ripe_age:
                        ok = self.__sync_file(f)
                        if ok:
                            marked.append(f)

                for f in marked:
                    WATCHED.pop(f)

                if self.should_stop: break
                time.sleep(self.active_wait)

        t = threading.Thread(target=__syncer)
        t.daemon=True
        t.start()
        
        self.__sync_thread = t
        self.backend_log.info("Starting Sync - done")

    def stop(self):
        self.backend_log.info("Stopping Sync")
        self.should_stop = True
        self.stopped = False

        # Signal stop
        self.observer.stop()
        # Wait
        self.__sync_thread.join()
        self.observer.join()
        self.should_stop = False
        self.stopped = True
        self.backend_log.info("Stopping Sync - done")
                
    def __sync_file(self, path):
        LOG.info("Syncing {}".format(path))

        if self.targets is None: return True  # No sync specified guess they don't want it...

        good = True
        for location in self.targets:
            err = subprocess.call('%s "%s" "%s"' %
                                   (settings['sync']['method'], path, location), shell=True)
            if err == 0:
                LOG.info("Syncing {} to {} succesfully".format(path, location))
                self.last.append(path)
            else:
                LOG.warning("Syncing {} to {} failed with error {}".format(path, location, err))

            good = good and err == 0  # ie. OK or not...
        return good

    def is_running(self):
        t = self.__sync_thread
        o = self.observer
        return t is not None and t.is_alive()\
            and o is not None and o.is_alive()

    def status(self):
        if not self.is_running():
            return "Stopped"
        elif len(WATCHED) == 0:
            return "Idle"
        else:
            return "Watching %d" % len(WATCHED)

    def state(self):
        if self.should_stop:
            return State.STOPPING
        elif self.stopped:
            return State.STOPPED
        elif self.is_running():
            return State.RUNNING
        else:
            return State.CRASHED


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created' or event.event_type == 'modified':
            if not event.src_path in WATCHED:
                LOG.info("Sync watching {}".format(event.src_path))
            
            WATCHED[event.src_path] = time.time()


class MockSync:
    def __init__(self, directory, targets, *_):
        self.directory = directory
        self.targets = targets
        self.running = None

        self.backend_log = logging.getLogger("backend")
        self.backend_log.info("Created MockSync")

        self.last = collections.deque(maxlen=settings['logs']['n_sync_log'])
        for s in reversed(util.get_last_synced(settings['logs']['n_sync_log'])):
            self.last.append(s)

    def stop(self):
        self.backend_log.info("Stopping MockSync")
        self.running = False
        self.backend_log.info("Stopping MockSync - done")

    def start(self):
        self.backend_log.info("Starting MockSync")
        self.running = True
        self.backend_log.info("Starting MockSync - done")

    def is_running(self):
        return self.running

    def status(self):
        if not self.is_running():
            return "Stopped"
        elif len(WATCHED) == 0:
            return "Idle"
        else:
            return "Watching %d" % len(WATCHED)

    def state(self):
        if self.running is None:
            return State.STANDBY
        elif self.running:
            return State.RUNNING
        else:
            return State.STOPPED

