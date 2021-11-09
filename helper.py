import os
import subprocess as sp

def is_sudo():
    return os.getuid() == 0

def run_cmd(cmd):
    sp.call(cmd, stdout=sp.DEVNULL, stderr=sp.DEVNULL, shell=True)

def set_hostname(hostname):
    run_cmd(f"hostnamectl set-hostname {hostname}")

class dnf:
    def do(cmd): # run an unimplemented command
        run_cmd(f"dnf {cmd}")
    def upgrade():
        run_cmd("dnf -y upgrade --refresh")

    def check():
        run_cmd("dnf check")

    def install(package, *args):
        cmd = f"dnf install -y {package}"
        for arg in args:
            cmd += " " + arg
        run_cmd(cmd)
    
    def group(operation, group, *args):
        cmd = f"dnf group {operation} {group}"
        for arg in args:
            cmd += " " + arg
        run_cmd(cmd)

    def group_update(group, *args):
        cmd = f"dnf groupupdate {group}"
        for arg in args:
            cmd += " " + arg
        run_cmd(cmd)
    
    def config_manager(operation, value):
        run_cmd(f"dnf config-manager --{operation} {value}")