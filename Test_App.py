#!/usr/bin/python

import os
import re
import subprocess
import sys
from pathlib import Path

from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

import helper
from logic.dnf import Dnf
from logic.flatpak import Flatpak
from logic.apt import Apt


# global vars
HOME = None
OS = None
PC = None
DE = None
GPU = None
##############

# A regular expression, to extract the % complete.
progress_re = re.compile("Total complete: (\d+)%")


def simple_percent_parser(output):
    """
    Matches lines using the progress_re regex,
    returning a single integer for the % progress.
    """
    m = progress_re.search(output)
    if m:
        pc_complete = m.group(1)
        return int(pc_complete)


def main():
    if not helper.is_sudo():
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


class Window2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.start_process
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)

        l = QVBoxLayout()

        l.addWidget(self.progress)
        l.addWidget(self.text)

        w = QWidget()
        w.setLayout(l)

        self.setCentralWidget(w)

    def message(self, s):
        self.text.appendPlainText(s)

    def start_process(self):
        self.message("Executing process")
        self.p = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
        self.p.readyReadStandardOutput.connect(self.handle_stdout)
        self.p.readyReadStandardError.connect(self.handle_stderr)
        self.p.stateChanged.connect(self.handle_state)
        self.p.finished.connect(self.process_finished)  # Clean up once complete.
        self.p.start("python3", ['dummy_script.py'])

    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")

        # Extract progress if it is in the data.
        progress = simple_percent_parser(stderr)
        if progress:
            self.progress.setValue(progress)
        self.message(stderr)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.message(stdout)

    def handle_state(self, state):
        states = {
            QProcess.NotRunning: 'Not running',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        self.message(f"State changed: {state_name}")

    def process_finished(self):
        self.message("Process finished.")
        self.p = None


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.gpu = GPU
        self.initUI()

    def initUI(self):

        vbox = QVBoxLayout()

        cb_drivers = QCheckBox("Install System configs and Drivers   (Recommended)", self)
        cb_gpu = QCheckBox(f"Install {self.gpu} drivers", self)
        cb_dropbox = QCheckBox('Install Dropbox')
        cb_nextcloud = QCheckBox('Install NextCloud')
        cb_google = QCheckBox('Install Google Cloud')
        cb_skype = QCheckBox('Install Skype')
        cb_zoom = QCheckBox('Install Zoom')
        cb_chrome = QCheckBox('Install Chrome')
        cb_chromium = QCheckBox('Install Chromium')
        
        btn = QPushButton("Start Install", self)

        cb_drivers.setChecked(True)

        vbox.addWidget(cb_drivers)
        vbox.addWidget(cb_gpu)
        vbox.addWidget(cb_dropbox)
        vbox.addWidget(cb_nextcloud)
        vbox.addWidget(cb_google)
        vbox.addWidget(cb_skype)
        vbox.addWidget(cb_zoom)
        vbox.addWidget(cb_chrome)
        vbox.addWidget(cb_chromium)
        vbox.addWidget(btn)

        vbox.addLayout(vbox)
        vbox.addSpacing(30)

        self.setLayout(vbox)

        self.move(300, 300)
        self.setGeometry(400, 400, 400, 400)
        self.setWindowTitle('QCheckBox')
        self.show()
        btn.clicked.connect(self.window2)

    def changeText(self, btn):

        self.label.setText(btn.text())

    def window2(self):                                             # <===
        self.w = Window2()
        self.w.show()
        self.hide()


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
        Dnf.upgrade()
        Dnf.check()
        # By default my machine is called localhost; hence, I rename it for better accessability on the network.
        helper.set_hostname("fedora")

        # Enable RPM Fusion
        helper.run_cmd("rpm -Uvh http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm")
        helper.run_cmd("rpm -Uvh http://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm")
        # Enable the RPM Fusion free and nonfree repositories.
        Dnf.group_update("core")
        Dnf.install("rpmfusion-free-release-tainted")
        Dnf.install("dnf-plugins-core")

        # Enable Fastest Mirror Plugin.
        helper.run_cmd("echo 'fastestmirror=true' | tee -a /etc/dnf/dnf.conf")
        helper.run_cmd("echo 'max_parallel_downloads=20' | tee -a /etc/dnf/dnf.conf")
        helper.run_cmd("echo 'deltarpm=true' | tee -a /etc/dnf/dnf.conf")

        # Install Flatpak, Snap and Fedy
        Flatpak.remote_add("flathub", "https://flathub.org/repo/flathub.flatpakrepo", "--if-not-exists")
        Flatpak.update()
        Dnf.install("snapd")
        helper.run_cmd("ln -s /var/lib/snapd/snap /snap") # "sudo snap refresh" AFTER REBOOT # for classic snap support
        Dnf.do("copr enable kwizart/fedy")
        Dnf.install("fedy")
        Flatpak.install("flatseal")
        
        # Install Codecs and VLC.
        Dnf.install("vlc")
        Dnf.group_update("sound-and-video")
        Dnf.install("libdvdcss")
        Dnf.install("lame\*", "--exclude=lame-devel")
        Dnf.group("upgrade", "Multimedia", "--with-optional")
        Dnf.config_manager("set-enabled", "fedora-cisco-openh264")
        Dnf.install("gstreamer1-plugin-openh264", "mozilla-openh264")
        
        # Update disk drivers.
        helper.run_cmd("fwupdmgr refresh --force")
        if "WARNING:" in subprocess.getoutput('fwupdmgr get-updates'):
            print("DEBUG:true")
            helper.run_cmd("echo 'DisabledPlugins=test;invalid;uefi' | tee -a /etc/fwupd/daemon.conf") # Remove WARNING: Firmware can not be updated in legacy BIOS mode.
        helper.run_cmd("fwupdmgr get-updates")
        helper.run_cmd("fwupdmgr update")
    
    elif OS == "Ubuntu":
        
        # Update system.
        Apt.update()
        Apt.upgrade()
        Apt.dist_upgrade()
        Apt.autoremove()
        Apt.autoclean()
        
        # Update disk drivers.
        helper.run_cmd("fwupdmgr get-devices")
        helper.run_cmd("fwupdmgr get-updates")
        helper.run_cmd("fwupdmgr update")
        # run_cmd("reboot now") # Nedds to save STATE if enable reboot.
        
        # System Utilities.
        Apt.install("snapd")
        Apt.install("flatpak")
        Flatpak.remote_add("flathub", "https://flathub.org/repo/flathub.flatpakrepo", "--if-not-exists")
        Flatpak.update()
        Flatpak.install("flatseal") # Tool to check or change the permissions of your flatpaks
        Apt.install("nautilus-admin")
        Apt.install("caffeine") # A little helper in case my laptop needs to stay up all night
        
        # Install Codecs and VLC.
        Apt.install("vlc")
        Apt.install("libavcodec-extra", "libdvd-pkg")
        helper.run_cmd("dpkg-reconfigure libdvd-pkg")
    elif PC == "Laptop":
        
        if OS == "Fedora":
            # Reduce Battery Usage - TLP.
            Dnf.install("tlp", "tlp-rdw")
            helper.run_cmd("systemctl enable tlp")
            
        if OS == "Ubuntu":
            helper.run_cmd("add-apt-repository ppa:linuxuprising/apps") # -y ??
            helper.run_cmd("apt-get update")
            helper.run_cmd("apt-get install tlp tlpui")
            helper.run_cmd("tlp start")


def install_gpu():

    if GPU == "Nvidia":
        helper.run_cmd("modinfo -F version nvidia")
        Dnf.install("akmod-nvidia") # rhel/centos users can use kmod-nvidia instead
        Dnf.install("xorg-x11-drv-nvidia-cuda") #optional for cuda/nvdec/nvenc support
        Dnf.install("xorg-x11-drv-nvidia-cuda-libs")
        Dnf.install("vdpauinfo", "libva-vdpau-driver", "libva-utils")
        Dnf.install("vulkan")
        helper.run_cmd("modinfo -F version nvidia")


def install_dropbox():
    if OS == "Fedora":
        Dnf.install("dropbox", "nautilus-dropbox")

    elif OS == "Ubuntu":
        Apt.install("nautilus-dropbox")


def install_nextcloud():
    if OS == "Fedora":
        Dnf.install("nextcloud-client", "nextcloud-client-nautilus")
        helper.run_cmd("-i")
        helper.run_cmd("echo 'fs.inotify.max_user_watches = 524288' >> /etc/sysctl.conf")
        helper.run_cmd("sysctl -p")
        
    elif OS == "Ubuntu":
        Apt.install("nextcloud-desktop")


def install_google():
    Dnf.install("python3-devel", "python3-pip", "python3-inotify", "python3-gobject", "cairo-devel", "cairo-gobject-devel", "libappindicator-gtk3")
    helper.run_cmd("python3 -m pip install --upgrade google-api-python-client")
    helper.run_cmd("python3 -m pip install --upgrade oauth2client")
    helper.run_cmd("yum install -y overgrive-3.3.*.noarch.rpm")


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
        helper.download_file("https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")
        helper.dpkg_install("google-chrome-stable_current_amd64.deb")


def install_chromium():
    if OS == "Fedora":
        Dnf.install("chromium")
        
    elif OS == "Ubuntu":
        Apt.install("chromium-browser")


def main():
    print('hello')
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


