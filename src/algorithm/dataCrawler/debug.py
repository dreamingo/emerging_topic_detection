from __future__ import print_function
import configure

LOG_FILE = "debug/debug.log"
_logFile = open(LOG_FILE, 'w')

def dprintf(*args, **kwargs):
    if not configure.DEBUG: return
    print(*args, file=_logFile)
    # print(*args)
