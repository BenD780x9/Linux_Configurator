import sys
from time import sleep
#want to deal with newlines as stream flushes
for line in open('install.txt').readlines():
    print(line)
    sys.stdout.flush()
    sleep(1)