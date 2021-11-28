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
        do("-y upgrade --refresh")

    def check():
        do("check")

    def install(package, *args):
        cmd = f"install -y {package}"
        for arg in args:
            cmd += " " + arg
        do(cmd)
    
    def group(operation, group, *args):
        cmd = f"group {operation} {group}"
        for arg in args:
            cmd += " " + arg
        do(cmd)

    def group_update(group, *args):
        cmd = f"groupupdate {group}"
        for arg in args:
            cmd += " " + arg
        do(cmd)
    
    def config_manager(operation, value):
        do(f"config-manager --{operation} {value}")

class flatpak:
    def do(cmd): # run an unimplemented command
        run_cmd(f"flatpak {cmd}")
    def update():
        do("update")

    def remote_add(name, url, *args):
        cmd = f"remote-add {name} {url}"
        for arg in args:
            cmd += " " + arg
        do(cmd)

    def install(package):
        do(f"install -y {package}")

class apt:
    def do(cmd): # run an unimplemented command
        run_cmd(f"apt {cmd}")

    def update():
        do("update")

    def upgrade():
        do("-y upgrade")

    def dist_upgrade():
        do("-y dist-upgrade")
    
    def autoremove():
        do("-y autoremove")
    
    def autoclean():
        do("-y autoclean")
    
    def install(package, *args):
        cmd = f"install -y {package}"
        for arg in args:
            cmd += " " + arg
        do(cmd)