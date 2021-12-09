from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QProcess
from helper import *
import re

from logic.facts import Facts
from logic.apt import Apt

class MainWindow(QWidget):
    def __init__(self, facts:Facts):
        super().__init__()
        self.facts = facts
        self.dic = {'cb_drivers':False, 'cb_gpu':False, 'cb_dropbox':False, 'cb_nextcloud':False, 'cb_google':False, 'cb_skype':False, 'cb_zoom':False, 'cb_chrome':False, 'cb_chromium':False}
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        
        self.label = QtWidgets.QLabel(f"You are runnig a {self.facts.PC} PC \nYour system is {self.facts.OS} with {self.facts.GPU} GPU.\n\nChoose what to install:")
        vbox.addWidget(self.label)
        
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
        
        self.btn = QPushButton("Start Install", self)
        vbox.addWidget(self.btn)
        self.btn.clicked.connect(self.start_installation)

        vbox.addSpacing(30)

        self.setLayout(vbox)

        self.move(300, 300)
        self.setGeometry(400, 400, 400, 400)
        self.setWindowTitle('QCheckBox')
        self.show()

    def checked(self): 
        """ If checked it change the value in the dictionery. 
            In the second window the installer checks what it need to (install True = install / False = NOT install) """
        
        if self.cb_drivers.checkState():
            self.dic['cb_drivers'] = True
            #print("DEBUG:Drivers")

        if self.cb_gpu.checkState():
            self.dic['cb_gpu'] = True
            #print("DEBUG:GPU drivers")

        if self.cb_dropbox.checkState():
            self.dic['cb_dropbox'] = True
            #print("DEBUG:dropbox")

        if self.cb_nextcloud.checkState():
            self.dic['cb_nextcloud'] = True
            #print("DEBUG:nextcloud")

        if self.cb_google.checkState():
            self.dic['cb_google'] = True
            #print("DEBUG:google")

        if self.cb_zoom.checkState():
            self.dic['cb_zoom'] = True
            #print("DEBUG:zoom")

        if self.cb_skype.checkState():
            self.dic['cb_skype'] = True
            #print("DEBUG:skype")

        if self.cb_chrome.checkState():
            self.dic['cb_chrome'] = True
            #print("DEBUG:chrome")

        if self.cb_chromium.checkState():
            self.dic['cb_chromium'] = True
            #print("DEBUG:chromium")
    
    def start_installation(self):
        self.win_install = WindowInstall(self.dic, self.facts)
        self.win_install.show()
        self.hide()


class WindowInstall(QMainWindow):
    def __init__(self, dic, facts):
        super().__init__()

        print(dic)
        self.facts = facts
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        self.start_process()

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)

        l = QVBoxLayout()
        #l.addWidget(self.btn)
        l.addWidget(self.progress)
        l.addWidget(self.text)

        w = QWidget()
        w.setLayout(l)

        self.setCentralWidget(w)
        self.setMinimumWidth(600)

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
        #self.p.start("bash", ['ls'])

    def simple_percent_parser(self, io):
        if type(self.facts.package_manager) is Apt:
            matches = re.findall("(?:^|\n|\r|(?:Do you want to continue? \[Y\/n] ))\(?((?:\S| \S)+) ?\.\.\.(?: ?(\d+)%)?", io)
            activity = None
            progress = None
            matches.reverse()
            for groups in matches:
                if activity is None:
                    activity = groups[0]
                progress = groups[1] if len(groups) >=2 else None
                if progress is not None and progress != '':
                    return activity, int(progress)
            return activity, None
        return None, None

    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")

        
        self.message(stderr)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        
        # Extract progress if it is in the data.
        activity, progress = self.simple_percent_parser(stdout)
        if activity:
            self.setWindowTitle(activity)
        if progress:
            self.progress.setValue(progress)
        self.message(stdout)

    def handle_state(self, state):
        states = {
            QProcess.NotRunning: 'Not running',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        self.setWindowTitle(state_name)
        self.message(f"State changed: {state_name}")

    def process_finished(self):
        self.message("Process finished.")
        self.p = None
