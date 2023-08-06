import urllib2
import json
import subprocess
import shlex

import time
import sys
import os

if len(sys.argv) == 1:
    print "No path to clewarecontrol supplied. Assuming ./clewarecontrol"

CLEWARECTRL = sys.argv[1] if len(sys.argv) == 2 else './clewarecontrol '
GREEN = 2
YELLOW = 1
RED = 0

ON = 1
OFF = 0

ALL_COLORS = [RED, YELLOW, GREEN]

FNULL = open(os.devnull, 'w')

def set_light(lights):
    cmd = " -c 1 "
    for i in range(3):
        cmd += "-as {} {} ".format(i, lights[i])

    subprocess.call(shlex.split("{} {}".format(CLEWARECTRL, cmd)), stdout=FNULL, stderr=FNULL)


def get_status():
    response = urllib2.urlopen('https://daqc.kern.phys.au.dk/api/status')
    html = response.read()
    return json.loads(html)


def check_status(args, good_states):
    for c in args:
        s = response[c]['status']
        status = s in good_states
        if not status:
            return False
    return True

critical = ['mbs', 'sync', 'sync', 'mesytec', 'vme']
essential = ['go4']
allowed_to_fail = ['file']

set_light([0]*3)

while True:
    try:
        response = get_status()
        common_status = True

        c_status = check_status(critical, ['running', 'stopped'])
        e_status = check_status(essential, ['running', 'stopped'])
        a_status = check_status(allowed_to_fail, ['running'])

        lights = [OFF]*3
        
        if c_status and e_status and a_status:
            lights[GREEN] = ON
        elif c_status and e_status:
            lights[YELLOW] = ON
        elif c_status:
            lights[YELLOW] = ON
            lights[RED] = ON
        else:
            lights[RED] = ON

        set_light(lights)
            
    except:
        set_light([ON]*3)

    time.sleep(1)



