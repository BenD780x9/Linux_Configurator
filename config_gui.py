from typing import Generator
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QProcess
from helper import *
import time
from PyQt5.QtCore import QThread, pyqtSignal
import sys
from logic.apt import Message
from functools import partial
import logic

dic = {'install_drivers': True, 'install_gpu': False, 'install_dropbox': False, 'install_nextcloud': False,
                    'install_google': False, 'install_skype': False, 'install_zoom': False, 'install_chrome': False,
                    'install_chromium': False}           

class MainWindow(QWidget):
    def __init__(self, facts):
        super().__init__()
        self.facts = facts
        self.dic = dic
        self.label = QtWidgets.QLabel(f"You are running a {self.facts.PC} PC.\nYour system is "
                                      f"{self.facts.OS} {self.facts.DE} with {self.facts.GPU} GPU.\n\n"
                                      f"Choose what to install:")
        self.cb_drivers = QCheckBox("Install System configs and Drivers   (Recommended)", self)
        self.cb_gpu = QCheckBox(f"Install {self.facts.GPU} drivers", self)
        self.cb_dropbox = QCheckBox('Install Dropbox')
        self.cb_nextcloud = QCheckBox('Install NextCloud')
        self.cb_google = QCheckBox('Install Google Cloud')
        self.cb_skype = QCheckBox('Install Skype')
        self.cb_zoom = QCheckBox('Install Zoom')
        self.cb_chrome = QCheckBox('Install Chrome')
        self.cb_chromium = QCheckBox('Install Chromium')
        self.btn = QPushButton("Start Install", self)
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        
        vbox.addSpacing(10)
        vbox.addWidget(self.label)
        
        vbox.addSpacing(10)
        vbox.addWidget(self.cb_drivers)
        self.cb_drivers.setChecked(True)
        self.cb_drivers.stateChanged.connect(self.checked)

        vbox.addWidget(self.cb_gpu)
        self.cb_gpu.stateChanged.connect(self.checked)
        
        vbox.addWidget(self.cb_dropbox)
        self.cb_dropbox.stateChanged.connect(self.checked)
        
        vbox.addWidget(self.cb_nextcloud)
        self.cb_nextcloud.stateChanged.connect(self.checked)

        vbox.addWidget(self.cb_google)
        self.cb_google.stateChanged.connect(self.checked)
        
        vbox.addWidget(self.cb_skype)
        self.cb_skype.stateChanged.connect(self.checked)
        
        vbox.addWidget(self.cb_zoom)
        self.cb_zoom.stateChanged.connect(self.checked)
        
        vbox.addWidget(self.cb_chrome)
        self.cb_chrome.stateChanged.connect(self.checked)
        
        vbox.addWidget(self.cb_chromium)
        self.cb_chromium.stateChanged.connect(self.checked)
        
        vbox.addSpacing(30)
        vbox.addWidget(self.btn)
        self.btn.clicked.connect(partial(self.start_installation, self.facts))

        vbox.addSpacing(30)

        self.setLayout(vbox)

        self.move(300, 300)
        self.setGeometry(400, 400, 400, 400)
        self.setWindowTitle('EZLinux')
        self.show()

    def checked(self): 
        """ If checked it change the value in the dictionary.
            In the second window the installer checks what it need to (install True = install / False = NOT install) """
        
        if self.cb_drivers.checkState():
            self.dic['install_drivers'] = True
        else:
            self.dic['install_drivers'] = False

        if self.cb_gpu.checkState():
            self.dic['install_gpu'] = True
        else:
            self.dic['install_gpu'] = False

        if self.cb_dropbox.checkState():
            self.dic['install_dropbox'] = True
        else:
            self.dic['install_dropbox'] = False

        if self.cb_nextcloud.checkState():
            self.dic['install_nextcloud'] = True
        else:
            self.dic['install_nextcloud'] = False

        if self.cb_google.checkState():
            self.dic['install_google'] = True
        else:
            self.dic['install_google'] = False

        if self.cb_zoom.checkState():
            self.dic['install_zoom'] = True
        else:
            self.dic['install_zoom'] = False

        if self.cb_skype.checkState():
            self.dic['install_skype'] = True
        else:
            self.dic['install_skype'] = False

        if self.cb_chrome.checkState():
            self.dic['install_chrome'] = True
        else:
            self.dic['install_chrome'] = False

        if self.cb_chromium.checkState():
            self.dic['install_chromium'] = True
        else:
            self.dic['install_chromium'] = False

    def start_installation(self, facts):
        self.win_install = InstallWindow(facts)

        self.win_install.show()
        self.hide()


class Installer(QThread):

    _signal = pyqtSignal(int)
    def __init__(self):
        super(Installer, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        for i in range(100):
            time.sleep(0.1)
            self._signal.emit(i)

class InstallWindow(QWidget):
    def __init__(self, facts):
        super(InstallWindow, self).__init__()

        self.facts = facts
        self.dic = dic
        self.Message = Message # For messages in "self.label"
        self.install_packages = [key for key, value in self.dic.items() if value == True] # Chck which installation needs to start.
          
        # Progress for pbar
        self.progress = int(100 / len(self.install_packages))
        self.first = range(0, self.progress)
        self.prog = self.progress
  
        self.d = {}
        for package in self.install_packages:
            if self.progress <= 100:
                # Changes the format for installation script.
                l = f"logic.{str.lower(self.facts.package_manager.__class__.__name__)}.{self.facts.package_manager.__class__.__name__}.{package}()"
                self.d[l] = self.progress
                self.progress = self.progress + self.prog

        """ ONLY for testing """
        #print(self.d)
        #print(self.facts.PC)
        # print(f"{len(self.install_packages)} items")
        # print(f"{self.prog} %")
        # print(self.prog * len(self.install_packages))
        
              
      
        # Window
        self.label = QtWidgets.QLabel(f"Install {l} package") # PUT the name of the package currenly being installing. 
        self.setWindowTitle('EZLinux')
        self.pbar = QProgressBar(self)
        #self.pbar.setValue(0) # 'progress' value
        self.resize(350, 100)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.pbar)
        self.setLayout(self.vbox)
        self.vbox.addWidget(self.label)
            
        self.show()
        self.installer = Installer()
        self.installer._signal.connect(self.signal_accept)
        self.installer.start()


    def signal_accept(self, value):
        self.pbar.setValue(value)

    """ Here if we want to work with in the future """
    # def btnFunc(self):
    #     self.WindowInstall = WindowInstall()
    #     self.WindowInstall._signal.connect(self.signal_accept)
    #     self.WindowInstall.start()
    #     self.btn.setEnabled(False)

    def signal_accept(self, msg):
            i = 0
            drivers = f"{self.facts.package_manager.__class__.__name__}.{self.facts.package_manager.__class__.__name__}.install_drivers()"
            while True:                
                for key in self.d: # List with pckages to install.
                    exec(key)
                    for i in range( i, self.d[key] ): # Set value for pbar.
                        time.sleep(0.1)
                        self.pbar.setValue(i)
                        if i == self.d[key] - 1:
                            i = self.d[key]
                            print(i)
                            if i == (len(self.install_packages) * self.prog): # Exit if Pbar in done.  
                                if drivers not in self.d: # No need to restart if drivers not installed.
                                    sys.exit()
                                else:
                                    sys.exit()
                                    # Add reboot after drivers installation.
                print(i)

    """ Here if we need a push button in the progress bar """
            #self.pbar.setValue(0)
            #self.btn.setEnabled(True)