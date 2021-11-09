import os
import subprocess as sp

def is_sudo():
    return os.getuid() == 0

def run_cmd(cmd):
    sp.call(cmd, stdout=sp.DEVNULL, stderr=sp.DEVNULL, shell=True)