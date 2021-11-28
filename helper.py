import os
import requests
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
