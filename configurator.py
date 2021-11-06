import sh
import os
import subprocess
import sys
import time
from pathlib import Path
from PyQt5.QtWidgets import *


HOME = str(Path.home())

"""Determine the Distro and Desktop Enviroment"""
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



"""Determine which GPU is in the PC"""
gpu = os.popen("lspci | grep VGA").read().lower()
if "intel" in gpu:
    GPU = "Intel"
elif "amd" in gpu:
    GPU = "AMD"
elif "nvidia" in gpu:
    GPU = "Nvidia"
else:
    GPU = "Unknown"

"""Determine if the computer is PC or a Laptop"""
if "No such file or directory" in subprocess.getoutput("ls cat /proc/acpi/button/lid"):
    PC = "Desktop"
else:
    PC = "Laptop"    

system = f"You are runnig a {PC} PC \nYour system is {OS} {DE} with {GPU} GPU."



def drivers():
    if OS == "Fedora":
        os.system("sudo dnf upgrade --refresh")
        os.system("sudo dnf check")
        os.system("hostnamectl set-hostname fedora") # By default my machine is called localhost; hence, I rename it for better accessability on the network.

        
        # Enable RPM Fusion
        os.system("sudo rpm -Uvh http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm")
        os.system("sudo rpm -Uvh http://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm")
        # Enable the RPM Fusion free and nonfree repositories.
        os.system("sudo dnf groupupdate core")
        os.system("sudo dnf install -y rpmfusion-free-release-tainted")
        os.system("sudo dnf install -y dnf-plugins-core")

        # Enable Fastest Mirror Plugin.
        print("Enable Fastest Mirror")
        os.system("echo 'fastestmirror=true' | sudo tee -a /etc/dnf/dnf.conf")
        os.system("echo 'max_parallel_downloads=20' | sudo tee -a /etc/dnf/dnf.conf")
        os.system("echo 'deltarpm=true' | sudo tee -a /etc/dnf/dnf.conf")

        # Install Flatpak, Snap and Fedy
        print("Install Flatpak, Snap and Fedy")
        os.system("flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo")
        os.system("flatpak update")
        os.system("sudo dnf install -y snapd")
        os.system("sudo ln -s /var/lib/snapd/snap /snap") # "sudo snap refresh" AFTER REBOOT # for classic snap support
        os.system("sudo dnf copr enable kwizart/fedy")
        os.system("sudo dnf install fedy -y")
        os.system("flatpak install -y flatseal")
        
        # Install Codecs and VLC.
        print("Install Codecs and VLC")
        os.system("sudo dnf install -y vlc")
        os.system("sudo dnf groupupdate sound-and-video")
        os.system("sudo dnf install -y libdvdcss")
        os.system("sudo dnf install -y lame\* --exclude=lame-devel")
        os.system("sudo dnf group upgrade --with-optional Multimedia")
        os.system("sudo dnf config-manager --set-enabled fedora-cisco-openh264")
        os.system("sudo dnf install -y gstreamer1-plugin-openh264 mozilla-openh264")  
        
        # Update disk drivers,
        os.system("sudo fwupdmgr refresh --force")
        if "WARNING:" in subprocess.getoutput('sudo fwupdmgr get-updates'):
            print("true")
            os.system("echo 'DisabledPlugins=test;invalid;uefi' | sudo tee -a /etc/fwupd/daemon.conf") # Remove WARNING: Firmware can not be updated in legacy BIOS mode.
        os.system("sudo fwupdmgr get-updates")
        os.system("sudo fwupdmgr update")

    elif PC == "Laptop":

        # Reduce Battery Usage - TLP.
        os.system("sudo dnf install tlp tlp-rdw")
        os.system("sudo systemctl enable tlp")

def install_gpu():

    if GPU == "Nvidia":
        os.system("modinfo -F version nvidia")
        os.system("sudo dnf install -y akmod-nvidia") # rhel/centos users can use kmod-nvidia instead
        os.system("sudo dnf install -y xorg-x11-drv-nvidia-cuda") #optional for cuda/nvdec/nvenc support
        os.system("sudo dnf install -y xorg-x11-drv-nvidia-cuda-libs")
        os.system("sudo dnf install -y vdpauinfo libva-vdpau-driver libva-utils")
        os.system("sudo dnf install -y vulkan")
        os.system("modinfo -F version nvidia")
    
    #elif GPU == "AMD": # Disable for now until we have installation process
        #os.system("xorg-x11-drv-amdgpu.x86_64")
        
        # Add file to X11 config, *NEED TO TEST IT BEFORE!
        #os.system('Section "Device"\n\tIdentifier "AMD"\n\tDriver "amdgpu"\nEndSection" > /etc/X11/xorg.conf.d/20-amdgpu.conf') 

    #elif GPU == "Intel": Disable for now until we have installation process    



 
def install_dropbox():
    os.system("sudo dnf install -y dropbox nautilus-dropbox")

def install_nextcloud():
    os.system("sudo dnf install -y nextcloud-client nextcloud-client-nautilus")
    os.system("sudo -i")
    os.system("echo 'fs.inotify.max_user_watches = 524288' >> /etc/sysctl.conf")
    os.system("sysctl -p")

def install_google():
    os.system("sudo dnf install -y python3-devel python3-pip python3-inotify python3-gobject cairo-devel cairo-gobject-devel libappindicator-gtk3")
    os.system("sudo python3 -m pip install --upgrade google-api-python-client")
    os.system("sudo python3 -m pip install --upgrade oauth2client")
    os.system("sudo yum install -y overgrive-3.3.*.noarch.rpm")

def install_skype():
    os.system("flatpak install -y skype")

def install_zoom():    
    os.system("flatpak install -y zoom")
        
def install_chrome():
    os.system("sudo dnf install -y fedora-workstation-repositories")
    os.system("sudo dnf config-manager --set-enabled google-chrome")
    os.system("sudo dnf install -y google-chrome-stable")
           
def install_chromium():    
    os.system("sudo dnf install -y chromium")

### APP ###

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Installer')
window.setGeometry(400, 400, 400, 400)
layout = QVBoxLayout()
label = QLabel(f'{system}\n\nChoose what to install')
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

# Check what box user check and install it.
# "checkState" check if box is chacked 0 is NO / 2 is YES
def install():
    d = {   'drivers': (cb_drivers.checkState()),
            'gpu': (cb_gpu.checkState()),
            'dropbox': (cb_dropbox.checkState()),
            'nextcloud': (cb_nextcloud.checkState()),
            'google': (cb_google.checkState()),
            'zoom': (cb_zoom.checkState()),
            'skype': (cb_skype.checkState()),
            'chrome': (cb_chrome.checkState()),
            'chromium': (cb_chromium.checkState()),
            }
    
    o = []
    filtered_dictionary = {}
    filtered_dictionary = {o.append(key) for key, value in d.items() if value == 2}
    print(o)     


btn = QPushButton('Start Install')
btn.clicked.connect(install)

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



