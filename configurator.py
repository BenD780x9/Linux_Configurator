#!/usr/bin/env python

import os
import subprocess
import sys
import time
from pathlib import Path
from functools import partial
from PyQt5.QtWidgets import *
from helper import *
from logic.dnf import Dnf
from logic.apt import Apt
from logic.flatpak import Flatpak

# global vars
HOME = None
OS = None
PC = None
DE = None
GPU = None
##############


def main():
    if not is_sudo():
        print("This script must be run as root") # replace with a QMessageBox not DEBUG
        sys.exit()

    HOME = str(Path.home())

    # Determine the Distro and Desktop Enviroment #
    distro = os.popen("cat /etc/*release").read()
    if "fedora" in distro:
        OS = "Fedora"
        if "KDE" in distro:
            DE = "KDE"
        else:
            DE = "GNOME"
    elif "ubuntu" in distro:
        OS = "Ubuntu"
        if "KDE" in distro:
            DE = "KDE"
        else:
            DE = "GNOME"

    # Determine which GPU is in the PC #
    gpu = os.popen("lspci | grep VGA").read().lower()
    if "intel" in gpu:
        GPU = "Intel"
    elif "amd" in gpu:
        GPU = "AMD"
    elif "nvidia" in gpu:
        GPU = "Nvidia"
    else:
        GPU = "Unknown"

    # Determine if the computer is PC or a Laptop #
    if not os.path.exists("/proc/acpi/button/lid"):
        PC = "Desktop"
    else:
        PC = "Laptop"    

    ### APP ###
    
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle('Installer')
    window.setGeometry(400, 400, 400, 400)
    layout = QVBoxLayout()
    infostr = f"You are runnig a {PC} PC \nYour system is {OS} {DE} with {GPU} GPU."
    label = QLabel(f'{infostr}\n\nChoose what to install')
    cb_drivers = QCheckBox(f"Install System configs and Drivers   (Recommended)")
    cb_gpu = QCheckBox(f"Install {GPU} drivers")
    cb_dropbox = QCheckBox('Install Dropbox')
    cb_nextcloud = QCheckBox('Install NextCloud')
    cb_google = QCheckBox('Install Google Cloud')
    cb_skype = QCheckBox('Install Skype')
    cb_zoom = QCheckBox('Install Zoom')
    cb_chrome = QCheckBox('Install Chrome')
    cb_chromium = QCheckBox('Install Chromium')
        
    cb_drivers.setChecked(True)

    btn = QPushButton('Start Install')
    install_func = partial(install, cb_drivers, cb_gpu, cb_dropbox, cb_nextcloud, cb_google, cb_zoom, cb_skype, cb_chrome, cb_chromium)
    btn.clicked.connect(install_func)

    layout.addWidget(label)

    layout.addWidget(cb_drivers)
    layout.addWidget(cb_gpu)
    layout.addWidget(cb_dropbox)
    layout.addWidget(cb_nextcloud)
    layout.addWidget(cb_google)
    layout.addWidget(cb_zoom)
    layout.addWidget(cb_skype)
    layout.addWidget(cb_chrome)
    layout.addWidget(cb_chromium)


    layout.addWidget(btn)
    window.setLayout(layout)
    window.show()
    sys.exit(app.exec_())


def install(drivers, gpu, dropbox, nextcloud, google, zoom, skype, chrome, chromium): # all booleans to indicate if installation needed
    print("DEBUG:We need to install:")
    if drivers.checkState():
        print("DEBUG:Drivers") # replace with install_drivers()
    if gpu.checkState():
        print("DEBUG:GPU drivers") # replace with install_gpu()
    if dropbox.checkState():
        print("DEBUG:dropbox") # replace with install_dropbox()
    if nextcloud.checkState():
        print("DEBUG:nextcloud") # replace with install_nextcloud()
    if google.checkState():
        print("DEBUG:google") # replace with install_google()
    if zoom.checkState():
        print("DEBUG:zoom") # replace with install_zoom()
    if skype.checkState():
        print("DEBUG:skype") # replace with install_skype()
    if chrome.checkState():
        print("DEBUG:chrome") # replace with install_chrome()
    if chromium.checkState():
        print("DEBUG:chromium") # replace with install_chromium()


def install_drivers():
    if OS == "Fedora":
        Dnf.install_drivers()

    elif OS == "Ubuntu":
        
        # Update system.
        Apt.install_drivers()

    elif PC == "Laptop":
        
        if OS == "Fedora":
            # Reduce Battery Usage - TLP.
            Dnf.install("tlp", "tlp-rdw")
            run_cmd("systemctl enable tlp")
            
        if OS == "Ubuntu":
            run_cmd("add-apt-repository ppa:linuxuprising/apps") # -y ??
            run_cmd("apt-get update")
            run_cmd("apt-get install tlp tlpui")
            run_cmd("tlp start")


def install_gpu():

    if GPU == "Nvidia":
        run_cmd("modinfo -F version nvidia")
        Dnf.install("akmod-nvidia") # rhel/centos users can use kmod-nvidia instead
        Dnf.install("xorg-x11-drv-nvidia-cuda") #optional for cuda/nvdec/nvenc support
        Dnf.install("xorg-x11-drv-nvidia-cuda-libs")
        Dnf.install("vdpauinfo", "libva-vdpau-driver", "libva-utils")
        Dnf.install("vulkan")
        run_cmd("modinfo -F version nvidia")
    
    #elif GPU == "AMD": # Disable for now until we have installation process
        #run_cmd("dnf install -y xorg-x11-drv-amdgpu.x86_64")
        
        # Creats AMD_GPU file to X11 config, *NEED TO TEST IT BEFORE!
        #run_cmd('Section "Device"\n\tIdentifier "AMD"\n\tDriver "amdgpu"\nEndSection" > /etc/X11/xorg.conf.d/20-amdgpu.conf') 

    #elif GPU == "Intel": Disable for now until we have installation process    


def install_dropbox():
    if OS == "Fedora":
        Dnf.install("dropbox", "nautilus-dropbox")

    elif OS == "Ubuntu":
        Apt.install("nautilus-dropbox")


def install_nextcloud():
    if OS == "Fedora":
        Dnf.install("nextcloud-client", "nextcloud-client-nautilus")
        run_cmd("-i")
        run_cmd("echo 'fs.inotify.max_user_watches = 524288' >> /etc/sysctl.conf")
        run_cmd("sysctl -p")
        
    elif OS == "Ubuntu":
        Apt.install("nextcloud-desktop")
        

def install_google():
    Dnf.install("python3-devel", "python3-pip", "python3-inotify", "python3-gobject", "cairo-devel", "cairo-gobject-devel", "libappindicator-gtk3")
    run_cmd("python3 -m pip install --upgrade google-api-python-client")
    run_cmd("python3 -m pip install --upgrade oauth2client")
    run_cmd("yum install -y overgrive-3.3.*.noarch.rpm")


def install_skype():
    Flatpak.install("skype")


def install_zoom():    
    Flatpak.install("zoom")
        

def install_chrome():
    if OS == "Fedora":
        Dnf.install("fedora-workstation-repositories")
        Dnf.config_manager("set-enabled", "google-chrome")
        Dnf.install("google-chrome-stable")
        
    elif OS == "Ubuntu":
        download_file("https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")
        dpkg_install("google-chrome-stable_current_amd64.deb")
        

def install_chromium():
    if OS == "Fedora":
        Dnf.install("chromium")
        
    elif OS == "Ubuntu":
        Apt.install("chromium-browser")


if __name__ == "__main__":
    main()
