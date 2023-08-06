import logging
import socket
import re
import time
import threading

from util import ReturningCommand

NAMES_END = '<<< TRIGGER NAMES END >>>'
NAMES_START = '<<< TRIGGER NAMES START >>>'
LINE_REGEXP = re.compile(r'(.*)\s*=\s*(\d*)')


class Trigger:
    def __init__(self, **kwargs):
        self.backend_log = logging.getLogger("backend")

        self.remote = kwargs.get('remote')
        if self.remote is None:
            raise ValueError("Missing remote hostname")

        self.port = kwargs.get('port')
        if self.port is None:
            raise ValueError("Missing remote port")

        self.trloctrl = kwargs.get('trloctrl')
        if self.trloctrl is None:
            raise ValueError("Missing trloctrl path")

        self.vulom_address = kwargs.get('vulom_address')
        if self.vulom_address is None:
            raise ValueError("Missing vulom address")

        self.name_cmd = kwargs.get('name_cmd')
        if self.name_cmd is None:
            raise ValueError("Missing name command")

        self.backend_log.info("Created Trigger")

        self.__real_trigger_names = False
        self.active_trigger = None
        self.tpat = [None]*16
        self.trig_red = [-1]*16
        self.compact_tpat = [None]*16
        self.trigger_names = ["-"]*16

        t = threading.Thread(target=self.__monitor)
        t.daemon = True
        t.start()

    def __monitor(self):
        while True:
            try:
                self.update_tpat()
                self.update_downscaling()
            except:
                pass

            time.sleep(1)

    def __request_mux(self, key):
        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        sock.settimeout(2)
        sock.sendto(key, (self.remote, self.port))
        return sock.recvfrom(4096)[0]

    def update_downscaling(self):
        res = self.__request_mux("SEND_TRIG_RED")

        split = res.split(',')
        if len(split) != 16: return

        self.trig_red = [int(x) for x in split]

    def update_tpat(self):
        res = self.__request_mux("SEND_TPAT")

        if len(res) == 16 and res != self.compact_tpat:
            active = ""
            for i in range(16):
                self.tpat[i] = res[i] == '1'
                if self.tpat[i]:
                    active += self.get_trigger_names()[i] + " + "

            if len(active) > 0:
                active = active[0:-3]

            self.active_trigger = active

    def set_trigger(self, trigger, downscaling):
        tpat = ','.join(map(str, trigger))

        cmd = "{} --addr={} tpat_enable={} ".format(self.trloctrl, self.vulom_address, tpat)
        for i, d in enumerate(downscaling):
            cmd += "'trig_red\[%d\]=%d' " % (i, d)

        stdout, _ = ReturningCommand(cmd).run().get()

        self.update_tpat()
        self.update_downscaling()

    def update_trigger_names(self):
        res, _ = ReturningCommand(self.name_cmd).run().get()
        begin = res.find(NAMES_START)
        end = res.find(NAMES_END)
        if begin == -1 or end == -1:
            return

        res = res[begin+len(NAMES_START):end]
        for line in res.split('\n'):
            line = line.strip()
            if len(line) == 0: continue

            match = LINE_REGEXP.match(line)
            if not match: continue

            i = int(match.group(2))
            if i < 1 or i > 16: continue
            name = match.group(1)

            self.trigger_names[i-1] = name

        # Now we got their real names:
        self.__real_trigger_names = True

    def get_trigger_names(self):
        if not self.__real_trigger_names:
            self.update_trigger_names()

        return self.trigger_names

    def get_active_trigger(self):
        return self.active_trigger

    def get_downscaling(self):
        return self.trig_red

class MockTrigger:
    def __init__(self, **kwargs):
        self.backend_log = logging.getLogger("backend")

        self.tpat = []
        for i in range(15):
            self.tpat.append(i % 4 == 0)
        self.tpat.append(None)

        self.downscaling = [0]*16

        self.compact_tpat = [None]*16
        self.trigger_names = []
        self.active_trigger = ""
        for i in range(16):
            self.trigger_names.append("T%d" % (i+1))

        self.__build_active_trigger()

        self.backend_log.info("Created MockTrigger")

    def set_trigger(self, trigger, new_downscaling):
        time.sleep(5)

        for i in trigger:
            if i < 1 or i > 16:
                raise ValueError("Trigger value must be >= 1 and <= 16")

        tpat = [False]*16
        for i in trigger:
            tpat[i-1] = True

        self.tpat = tpat
        self.downscaling = new_downscaling
        self.__build_active_trigger()


    def __build_active_trigger(self):
        active = ""
        for i in range(16):
            if self.tpat[i]:
                active += self.trigger_names[i] + " + "

        if len(active) > 0:
            active = active[0:-3]

        self.active_trigger = active

    def update_tpat(self):
        pass

    def update_trigger_names(self):
        from random import shuffle
        shuffle(self.trigger_names)

    def get_trigger_names(self):
        return self.trigger_names

    def get_active_trigger(self):
        return self.active_trigger

    def get_downscaling(self):
        return self.downscaling
