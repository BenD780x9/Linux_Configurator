#!/usr/bin/python

from PyQt5.QtCore import QProcess
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import re
import helper
#import ProgressWindow

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


dic = {'cb_drivers':0, 'cb_gpu':0, 'cb_dropbox':0, 'cb_nextcloud':0, 'cb_google':0, 'cb_skype':0, 'cb_zoom':0, 'cb_chrome':0, 'cb_chromium':0}

class Window2(QMainWindow):                           # <===
    #def __init__(self):
    #    super().__init__()
    #    self.setWindowTitle("Installation Progress")

     
    def __init__(self):
        super().__init__()

        #self.p = None

        #self.btn = QPushButton("Execute")
        #self.btn.pressed.connect(self.start_process)
        print(dic)
        self.start_process
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)

        l = QVBoxLayout()
        #l.addWidget(self.btn)
        l.addWidget(self.progress)
        l.addWidget(self.text)

        w = QWidget()
        w.setLayout(l)

        self.setCentralWidget(w)

    def message(self, s):
        self.text.appendPlainText(s)

    def start_process(self):
        #if self.p is None:  # No process running.
        self.message("Executing process")
        self.p = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
        self.p.readyReadStandardOutput.connect(self.handle_stdout)
        self.p.readyReadStandardError.connect(self.handle_stderr)
        self.p.stateChanged.connect(self.handle_state)
        self.p.finished.connect(self.process_finished)  # Clean up once complete.
        #self.p.start(install_func)
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
        
        #infostr = f"You are runnig a {PC} PC \nYour system is {OS} {DE} with {GPU} GPU."
        #self.label = QtWidgets.QLabel(self.centralwidget)
        #self.label.setGeometry(QtCore.QRect(14, 80, 500, 20))

        self.cb_drivers = QCheckBox("Install System configs and Drivers   (Recommended)", self)
        vbox.addWidget(self.cb_drivers)
        self.cb_drivers.setChecked(True)
        self.cb_drivers.stateChanged.connect(self.checked)

        self.cb_gpu = QCheckBox(f"Install {self.gpu} drivers", self)
        vbox.addWidget(self.cb_gpu)
        self.cb_gpu.stateChanged.connect(self.checked)
        
        self.cb_dropbox = QCheckBox('Install Dropbox')
        vbox.addWidget(self.cb_dropbox)
        self.cb_dropbox.stateChanged.connect(self.checked)
        
        self.cb_nextcloud = QCheckBox('Install NextCloud')
        vbox.addWidget(self.cb_nextcloud)
        self.cb_nextcloud.stateChanged.connect(self.checked)

        self.cb_google = QCheckBox('Install Google Cloud')
        vbox.addWidget(self.cb_google)
        self.cb_google.stateChanged.connect(self.checked)
        
        self.cb_skype = QCheckBox('Install Skype')
        vbox.addWidget(self.cb_skype)
        self.cb_skype.stateChanged.connect(self.checked)
        
        self.cb_zoom = QCheckBox('Install Zoom')
        vbox.addWidget(self.cb_zoom)
        self.cb_zoom.stateChanged.connect(self.checked)
        
        self.cb_chrome = QCheckBox('Install Chrome')
        vbox.addWidget(self.cb_chrome)
        self.cb_chrome.stateChanged.connect(self.checked)
        
        self.cb_chromium = QCheckBox('Install Chromium')
        vbox.addWidget(self.cb_chromium)
        self.cb_chromium.stateChanged.connect(self.checked)
        
        #btn = QPushButton('Start Install')
        self.btn = QPushButton("Start Install", self)
        vbox.addWidget(self.btn) 
            
        #group.buttonClicked.connect(self.changeText)

        #self.label = QLabel('...', self)

        vbox.addLayout(vbox)
        vbox.addSpacing(30)
        #vbox.addWidget(self.label)

        self.setLayout(vbox)

        self.move(300, 300)
        self.setGeometry(400, 400, 400, 400)
        self.setWindowTitle('QCheckBox')
        self.show()
        self.btn.clicked.connect(self.window2)
        #btn.clicked.connect(self.ProgressWindow)

    def checked(self): 
        """ If checked it change the value in the dictionery. 
            In the second window the installer checks what it need to (install 1 = install / 0 = NOT install) """
        
        if self.cb_drivers.checkState():
            dic['cb_drivers'] = 1
            print("DEBUG:Drivers") # replace with install_drivers()

        if self.cb_gpu.checkState():
            dic['cb_gpu'] = 1
            print("DEBUG:GPU drivers") # replace with install_gpu()

        if self.cb_dropbox.checkState():
            dic['cb_dropbox'] = 1
            print("DEBUG:dropbox") # replace with install_dropbox()

        if self.cb_nextcloud.checkState():
            dic['cb_nextcloud'] = 1
            print("DEBUG:nextcloud") # replace with install_nextcloud()

        if self.cb_google.checkState():
            dic['cb_google'] = 1
            print("DEBUG:google") # replace with install_google()

        if self.cb_zoom.checkState():
            dic['cb_zoom'] = 1
            print("DEBUG:zoom") # replace with install_zoom()

        if self.cb_skype.checkState():
            dic['cb_skype'] = 1
            print("DEBUG:skype") # replace with install_skype()

        if self.cb_chrome.checkState():
            dic['cb_chrome'] = 1
            print("DEBUG:chrome") # replace with install_chrome()

        if self.cb_chromium.checkState():
            dic['cb_chromium'] = 1
            print("DEBUG:chromium") # replace with install_chromium()

        


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
        dnf.upgrade()
        dnf.check()
        set_hostname("fedora") # By default my machine is called localhost; hence, I rename it for better accessability on the network.

        
        # Enable RPM Fusion
        run_cmd("rpm -Uvh http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm")
        run_cmd("rpm -Uvh http://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm")
        # Enable the RPM Fusion free and nonfree repositories.
        dnf.group_update("core")
        dnf.install("rpmfusion-free-release-tainted")
        dnf.install("dnf-plugins-core")

        # Enable Fastest Mirror Plugin.
        run_cmd("echo 'fastestmirror=true' | tee -a /etc/dnf/dnf.conf")
        run_cmd("echo 'max_parallel_downloads=20' | tee -a /etc/dnf/dnf.conf")
        run_cmd("echo 'deltarpm=true' | tee -a /etc/dnf/dnf.conf")

        # Install Flatpak, Snap and Fedy
        flatpak.remote_add("flathub", "https://flathub.org/repo/flathub.flatpakrepo", "--if-not-exists")
        flatpak.update()
        dnf.install("snapd")
        run_cmd("ln -s /var/lib/snapd/snap /snap") # "sudo snap refresh" AFTER REBOOT # for classic snap support
        dnf.do("copr enable kwizart/fedy")
        dnf.install("fedy")
        flatpak.install("flatseal")
        
        # Install Codecs and VLC.
        dnf.install("vlc")
        dnf.group_update("sound-and-video")
        dnf.install("libdvdcss")
        dnf.install("lame\*", "--exclude=lame-devel")
        dnf.group("upgrade", "Multimedia", "--with-optional")
        dnf.config_manager("set-enabled", "fedora-cisco-openh264")
        dnf.install("gstreamer1-plugin-openh264", "mozilla-openh264")
        
        # Update disk drivers.
        run_cmd("fwupdmgr refresh --force")
        if "WARNING:" in subprocess.getoutput('fwupdmgr get-updates'):
            print("DEBUG:true")
            run_cmd("echo 'DisabledPlugins=test;invalid;uefi' | tee -a /etc/fwupd/daemon.conf") # Remove WARNING: Firmware can not be updated in legacy BIOS mode.
        run_cmd("fwupdmgr get-updates")
        run_cmd("fwupdmgr update")
    
    elif OS == "Ubuntu":
        
        # Update system.
        apt.update()
        apt.upgrade()
        apt.dist_upgrade()
        apt.autoremove()
        apt.autoclean()
        
        # Update disk drivers.
        run_cmd("fwupdmgr get-devices")
        run_cmd("fwupdmgr get-updates")
        run_cmd("fwupdmgr update")
        # run_cmd("reboot now") # Nedds to save STATE if enable reboot.
        
        # System Utilities.
        apt.install("snapd")
        apt.install("flatpak")
        flatpak.remote_add("flathub", "https://flathub.org/repo/flathub.flatpakrepo", "--if-not-exists")
        flatpak.update()
        flatpak.install("flatseal") # Tool to check or change the permissions of your flatpaks
        apt.install("nautilus-admin")
        apt.install("caffeine") # A little helper in case my laptop needs to stay up all night
        
        # Install Codecs and VLC.
        apt.install("vlc")
        apt.install("libavcodec-extra", "libdvd-pkg")
        run_cmd("dpkg-reconfigure libdvd-pkg")
        
      
    elif PC == "Laptop":
        
        if OS == "Fedora":
            # Reduce Battery Usage - TLP.
            dnf.install("tlp", "tlp-rdw")
            run_cmd("systemctl enable tlp")
            
        if OS == "Ubuntu":
            run_cmd("add-apt-repository ppa:linuxuprising/apps") # -y ??
            run_cmd("apt-get update")
            run_cmd("apt-get install tlp tlpui")
            run_cmd("tlp start")

def install_gpu():

    if GPU == "Nvidia":
        run_cmd("modinfo -F version nvidia")
        dnf.install("akmod-nvidia") # rhel/centos users can use kmod-nvidia instead
        dnf.install("xorg-x11-drv-nvidia-cuda") #optional for cuda/nvdec/nvenc support
        dnf.install("xorg-x11-drv-nvidia-cuda-libs")
        dnf.install("vdpauinfo", "libva-vdpau-driver", "libva-utils")
        dnf.install("vulkan")
        run_cmd("modinfo -F version nvidia")
    
    #elif GPU == "AMD": # Disable for now until we have installation process
        #run_cmd("dnf install -y xorg-x11-drv-amdgpu.x86_64")
        
        # Creats AMD_GPU file to X11 config, *NEED TO TEST IT BEFORE!
        #run_cmd('Section "Device"\n\tIdentifier "AMD"\n\tDriver "amdgpu"\nEndSection" > /etc/X11/xorg.conf.d/20-amdgpu.conf') 

    #elif GPU == "Intel": Disable for now until we have installation process    
 
def install_dropbox():
    if OS == "Fedora":
        dnf.install("dropbox", "nautilus-dropbox")

    elif OS == "Ubuntu":
        apt.install("nautilus-dropbox")
        
def install_nextcloud():
    if OS == "Fedora":
        dnf.install("nextcloud-client", "nextcloud-client-nautilus")
        run_cmd("-i")
        run_cmd("echo 'fs.inotify.max_user_watches = 524288' >> /etc/sysctl.conf")
        run_cmd("sysctl -p")
        
    elif OS == "Ubuntu":
        apt.install("nextcloud-desktop")
        

def install_google():
    dnf.install("python3-devel", "python3-pip", "python3-inotify", "python3-gobject", "cairo-devel", "cairo-gobject-devel", "libappindicator-gtk3")
    run_cmd("python3 -m pip install --upgrade google-api-python-client")
    run_cmd("python3 -m pip install --upgrade oauth2client")
    run_cmd("yum install -y overgrive-3.3.*.noarch.rpm")

def install_skype():
    flatpak.install("skype")

def install_zoom():    
    flatpak.install("zoom")
        
def install_chrome():
    if OS == "Fedora":
        dnf.install("fedora-workstation-repositories")
        dnf.config_manager("set-enabled", "google-chrome")
        dnf.install("google-chrome-stable")
        
    elif OS == "Ubuntu":
        download_file("https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")
        dpkg_install("google-chrome-stable_current_amd64.deb")
        
def install_chromium():
    if OS == "Fedora":
        dnf.install("chromium")
        
    elif OS == "Ubuntu":
        apt.install("chromium-browser")


def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()



