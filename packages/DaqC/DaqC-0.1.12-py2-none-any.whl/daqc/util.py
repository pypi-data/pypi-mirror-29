import subprocess, threading
import time
import datetime
import stat
import re
import logging
import collections
import glob
from settings import settings
import os
import pytz

import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

#-----------------------
def write_file(filename, data):
   f=open(filename, "w")
   f.write(str(data))
   f.close()

#-----------------------
def append_file(filename, data):
   f=open(filename, "a")
   f.write(str(data))
   f.close()


#------------------------
def read_file(filename):
   f = open(filename, "r")
   n = f.read()
   f.close()
   return n


def remove_write_permissions(path):
    """Remove write permissions from this path, while keeping all other permissions intact.

    Params:
        path:  The path whose permissions to alter.
    """
    NO_USER_WRITING = ~stat.S_IWUSR
    NO_GROUP_WRITING = ~stat.S_IWGRP
    NO_OTHER_WRITING = ~stat.S_IWOTH
    NO_WRITING = NO_USER_WRITING & NO_GROUP_WRITING & NO_OTHER_WRITING

    current_permissions = stat.S_IMODE(os.lstat(path).st_mode)
    os.chmod(path, current_permissions & NO_WRITING)

#------------------------
def find_nth(s, x, n=0, overlap=False):
    l = 1 if overlap else len(x)
    i = -l
    for c in xrange(n):
        i = s.find(x, i + l)
        if i < 0:
            break
    return i


DEV_NULL = open(os.devnull, 'w')
utc = pytz.timezone('UTC')


def get_open_port():
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", 0))
        port = s.getsockname()[1]
        s.close()
        return port

#------------------------
def build_timestamp():
   return str(utc.localize(datetime.datetime.utcnow()))

class RunNumber:
    def __init__(self):
        run_file = settings['file_taking']['run_number_file']
        try:
            run_number=int(read_file(run_file))
        except:
            write_file(run_file, "0")
            run_number = 0

        self.current = run_number

    def get_current(self):
        return self.current

    def determine_next(self):
        ret = self.current
        try:
            os.chdir(settings.DATA_DIR)
            for file in glob.glob("*.lmd.gz"):
                m = re.search(r'\d+\.lmd.gz', file).group()
                ret = max(ret, int(m[0:-4]))
                return ret + 1
        except:
            return ret+1

    def increment_to_next(self):
        self.current = self.determine_next()
        write_file(settings['file_taking']['run_number_file'], self.current)

#------------------------
class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def run(self, timeout):
        def target():
            self.process = subprocess.Popen(self.cmd, stderr=subprocess.PIPE, shell=True)
            self.process.communicate()

        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()

        thread.join(timeout)
        while thread.is_alive():
            self.process.terminate()
            
        thread.join()


class ReturningCommand(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None
        self.thread = None
        self.result = None

    def run(self):
        def target():
            self.process = subprocess.Popen("exec " + self.cmd, stderr=subprocess.PIPE,\
                                            stdout=subprocess.PIPE, shell=True)
            self.result = self.process.communicate()

        self.thread = threading.Thread(target=target)
        self.thread.daemon = True
        self.thread.start()
        return self

    def get(self):
        self.thread.join()
        return self.result

    def is_running(self):
        return self.thread.is_alive() if self.thread is not None else False

    def terminate(self):
        self.process.terminate()

    def kill(self):
        self.process.kill()


def get_disk_space(dir):
    if not os.path.isdir(dir):
        return [float('nan'), float('nan'), float('nan')]
    c = ReturningCommand("df -k {}".format(dir)).run().get()
    # First is total, second is used and third is available in kilobytes!
    m = re.search("\s(\d+)\s+(\d+)\s+(\d+)", c[0])
    return [int(x) for x in m.groups(0)]


def get_files_from_run_log(filename):
    result = []
    if not os.path.exists(filename):
        return result

    with open(filename, 'rb') as f:
        data = yaml.safe_load(f.read())
        if data is None:
            return result

    for key, val in data.iteritems():
        e = dict()
        e.update({"run_number": key})
        e.update(val)
        result.append(RunFile(e))

    #
    result.sort(key=lambda entry: entry.get_run_nr())

    return result


def get_nr_files(wildcard):
    return len(glob.glob(wildcard))


def get_last_synced(cap=2):
    #    lines = []
    #    if not os.path.exists("daqc.log"):
    #        return lines

    #    with open("daqc.log", 'r') as f:
    #        lines = f.readlines()

    #    s = []
    #    for line in reversed(lines):
    #        if len(s) == cap: break
    #        m = re.search("Syncing.+\/(.+.lmd.gz).+succesfully",line)
    #        if m is not None:
    #            s.append(m.groups()[0])
    #    return s
    # All very inefficient
    return []

def sanitize(string):
    return os.path.basename(str(string)).replace(" ", "_")


class RAMHandler(logging.Handler):
        def __init__(self, maxlen):
                logging.Handler.__init__(self)
                self.messages = collections.deque(maxlen=maxlen)

        def emit(self, record):
                self.messages.append({'message': self.format(record), 'level': record.levelname})

        def get_messages(self):
            return list(self.messages)


NR = "run_number"

class RunFile:
    def __init__(self, info=None):
        if info is not None:
            self.info = info
        else:
            r = RunNumber()
            r.increment_to_next()
            self.info = {NR: r.get_current()}
        self.log = None
        self.on_log =[]

    def get_run_nr(self):
        return self.info[NR]

    def set_info(self, info):
        if NR in info:
            info.pop(NR)

        for key, value in info.iteritems():
            self.info[key] = value

    def get_yaml(self):
        result = "{}:\n".format(self.get_run_nr())
        for key, val in self.info.iteritems():
            if key == NR: continue
            result += "   {}: '{}'\n".format(key, val)

        return result

    def set_stop(self):
        timestamp = build_timestamp()
        self.set_info({"stop_time": timestamp})
        return timestamp

    def set_start(self):
        timestamp = build_timestamp()
        self.set_info({"start_time": timestamp})
        return timestamp

    def __fire_log_listener(self, log):
        for listener in self.on_log:
            listener(log)

    def set_log(self, log):
        self.log = log
        self.__fire_log_listener(log)

    def set_on_log(self, l):
        if self.log is not None:
            l(self.log)
        else:
            self.on_log.append(l)


def read_n_from_socket(socket, n_bytes):
    buf = bytearray(n_bytes)
    view = memoryview(buf)
    missing = n_bytes
    while missing > 0:
        received = socket.recv_into(view, missing)
        view = view[received:]
        missing -= received
    return buf

class RunDBState:
    def __init__(self):
        self.shouldUpload = True

    def start(self):
        self.shouldUpload = True

    def stop(self):
        self.shouldUpload = False


from logging.handlers import BaseRotatingHandler

class CustomRotatingFileHandler(BaseRotatingHandler):
    """
    Handler for logging to a set of files, which switches from one file
    to the next when the current file reaches a certain size.
    """

    def __init__(self, filename, maxBytes, backupdir, encoding=None, delay=0):

        BaseRotatingHandler.__init__(self, filename, 'a', encoding, delay)
        self.maxBytes = maxBytes
        self.backupdir = os.path.abspath(backupdir)
        if not os.path.exists(backupdir):
            os.mkdir(backupdir)

    def doRollover(self):
        """
        Do a rollover, as described in __init__().
        """
        if self.stream:
            self.stream.close()
            self.stream = None

        timestamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        _, fname = os.path.split(self.baseFilename)
        destination_file_name = os.path.join(self.backupdir, "{}_{}".format(timestamp, fname))
        print("{} -> {}".format(self.baseFilename, destination_file_name))
        os.rename(self.baseFilename, destination_file_name)

        self.stream = self._open()

    def shouldRollover(self, record):
        """
        Determine if rollover should occur.

        Basically, see if the supplied record would cause the file to exceed
        the size limit we have.
        """
        if self.stream is None:  # delay was set...
            self.stream = self._open()
        if self.maxBytes > 0:  # are we rolling over?
            msg = "%s\n" % self.format(record)
            self.stream.seek(0, 2)  # due to non-posix-compliant Windows feature
            if self.stream.tell() + len(msg) >= self.maxBytes:
                return 1
        return 0
