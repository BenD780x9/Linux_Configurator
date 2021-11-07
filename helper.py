import os

def is_sudo():
    return os.getuid() == 0