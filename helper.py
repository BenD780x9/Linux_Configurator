import os, requests
import subprocess as sp

def is_sudo():
    return os.getuid() == 0

def run_cmd(cmd):
    sp.call(cmd, stdout=sp.DEVNULL, stderr=sp.DEVNULL, shell=True)

def set_hostname(hostname):
    run_cmd(f"hostnamectl set-hostname {hostname}")

def dpkg_install(package):
    run_cmd(f"dpkg -i {package}")

def download_file(url):
    file = requests.get(url)
    open(url.split("/")[-1], 'wb').write(file.content)

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

class flatpak:
    def do(cmd): # run an unimplemented command
        run_cmd(f"flatpak {cmd}")
    def update():
        run_cmd("flatpak update")

    def remote_add(name, url, *args):
        cmd = f"flatpak remote-add {name} {url}"
        for arg in args:
            cmd += " " + arg
        run_cmd(cmd)

    def install(package):
        run_cmd(f"flatpak install -y {package}")

class apt:
    def do(cmd): # run an unimplemented command
        run_cmd(f"apt {cmd}")

    def update():
        run_cmd("apt update")

    def upgrade():
        run_cmd("apt -y upgrade")

    def dist_upgrade():
        run_cmd("apt -y dist-upgrade")
    
    def autoremove():
        run_cmd("apt -y autoremove")
    
    def autoclean():
        run_cmd("apt -y autoclean")
    
    def install(package, *args):
        cmd = f"apt install -y {package}"
        for arg in args:
            cmd += " " + arg
        run_cmd(cmd)