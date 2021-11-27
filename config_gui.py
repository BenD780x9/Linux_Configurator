from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QProcess
from helper import *

class MainWindow(QWidget):
    def __init__(self, facts):
        super().__init__()
        self.facts = facts
        self.initUI()
        self.dic = {'cb_drivers':0, 'cb_gpu':0, 'cb_dropbox':0, 'cb_nextcloud':0, 'cb_google':0, 'cb_skype':0, 'cb_zoom':0, 'cb_chrome':0, 'cb_chromium':0}

    def initUI(self):
        vbox = QVBoxLayout()

        self.cb_drivers = QCheckBox("Install System configs and Drivers   (Recommended)", self)
        vbox.addWidget(self.cb_drivers)
        self.cb_drivers.setChecked(True)
        self.cb_drivers.stateChanged.connect(self.checked)

        self.cb_gpu = QCheckBox(f"Install {self.facts.GPU} drivers", self)
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

        vbox.addLayout(vbox)
        vbox.addSpacing(30)

        self.setLayout(vbox)

        self.move(300, 300)
        self.setGeometry(400, 400, 400, 400)
        self.setWindowTitle('QCheckBox')
        self.show()

    def checked(self): 
        """ If checked it change the value in the dictionery. 
            In the second window the installer checks what it need to (install 1 = install / 0 = NOT install) """
        
        if self.cb_drivers.checkState():
            self.dic['cb_drivers'] = 1
            print("DEBUG:Drivers") # replace with install_drivers()

        if self.cb_gpu.checkState():
            self.dic['cb_gpu'] = 1
            print("DEBUG:GPU drivers") # replace with install_gpu()

        if self.cb_dropbox.checkState():
            self.dic['cb_dropbox'] = 1
            print("DEBUG:dropbox") # replace with install_dropbox()

        if self.cb_nextcloud.checkState():
            self.dic['cb_nextcloud'] = 1
            print("DEBUG:nextcloud") # replace with install_nextcloud()

        if self.cb_google.checkState():
            self.dic['cb_google'] = 1
            print("DEBUG:google") # replace with install_google()

        if self.cb_zoom.checkState():
            self.dic['cb_zoom'] = 1
            print("DEBUG:zoom") # replace with install_zoom()

        if self.cb_skype.checkState():
            self.dic['cb_skype'] = 1
            print("DEBUG:skype") # replace with install_skype()

        if self.cb_chrome.checkState():
            self.dic['cb_chrome'] = 1
            print("DEBUG:chrome") # replace with install_chrome()

        if self.cb_chromium.checkState():
            self.dic['cb_chromium'] = 1
            print("DEBUG:chromium") # replace with install_chromium()