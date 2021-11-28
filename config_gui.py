from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QProcess
from helper import *


class MainWindow(QWidget):
    def __init__(self, facts):
        super().__init__()
        self.facts = facts
        self.dic = {'cb_drivers': False, 'cb_gpu': False, 'cb_dropbox': False, 'cb_nextcloud': False,
                    'cb_google': False, 'cb_skype': False, 'cb_zoom': False, 'cb_chrome': False,
                    'cb_chromium': False}
        self.label = QtWidgets.QLabel(f"You are running a {self.facts.PC} PC \nYour package manager is "
                                      f"{self.facts.package_manager.__class__.__name__} with {self.facts.GPU} GPU.\n\n"
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
        
        vbox.addWidget(self.label)
        
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
        
        vbox.addWidget(self.btn)
        self.btn.clicked.connect(self.start_installation)

        vbox.addSpacing(30)

        self.setLayout(vbox)

        self.move(300, 300)
        self.setGeometry(400, 400, 400, 400)
        self.setWindowTitle('QCheckBox')
        self.show()

    def checked(self): 
        """ If checked it change the value in the dictionary.
            In the second window the installer checks what it need to (install True = install / False = NOT install) """
        
        if self.cb_drivers.checkState():
            self.dic['cb_drivers'] = True
        else:
            self.dic['cb_drivers'] = False

        if self.cb_gpu.checkState():
            self.dic['cb_gpu'] = True
        else:
            self.dic['cb_gpu'] = False

        if self.cb_dropbox.checkState():
            self.dic['cb_dropbox'] = True
        else:
            self.dic['cb_dropbox'] = False

        if self.cb_nextcloud.checkState():
            self.dic['cb_nextcloud'] = True
        else:
            self.dic['cb_nextcloud'] = False

        if self.cb_google.checkState():
            self.dic['cb_google'] = True
        else:
            self.dic['cb_google'] = False

        if self.cb_zoom.checkState():
            self.dic['cb_zoom'] = True
        else:
            self.dic['cb_zoom'] = False

        if self.cb_skype.checkState():
            self.dic['cb_skype'] = True
        else:
            self.dic['cb_skype'] = False

        if self.cb_chrome.checkState():
            self.dic['cb_chrome'] = True
        else:
            self.dic['cb_chrome'] = False

        if self.cb_chromium.checkState():
            self.dic['cb_chromium'] = True
        else:
            self.dic['cb_chromium'] = False

    def start_installation(self):
        self.win_install = WindowInstall(self.dic)
        self.win_install.show()
        self.hide()


class WindowInstall(QMainWindow):
    def __init__(self, dic):
        super().__init__()

        print(dic)
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
