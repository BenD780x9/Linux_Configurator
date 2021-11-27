import os
import subprocess
import sys
import time
from pathlib import Path
from functools import partial
from helper import *
from config_installer import *

def main():
    facts = Facts()
    if not is_sudo():
        print("This script must be run as root") # replace with a QMessageBox not DEBUG
        sys.exit()
    collect_facts(facts)

def collect_facts(facts):
    facts.HOME = str(Path.home())

    # Determine the Distro and Desktop Enviroment #
    distro = os.popen("cat /etc/*release").read()
    if "fedora" in distro:
        facts.OS = "Fedora"
        if "KDE" in distro:
            facts.DE = "KDE"
        else:
            facts.DE = "GNOME"
    elif "ubuntu" in distro:
        facts.OS = "Ubuntu"
        if "KDE" in distro:
            facts.DE = "KDE"
        else:
            facts.DE = "GNOME"

    # Determine which GPU is in the PC #
    gpu = os.popen("lspci | grep VGA").read().lower()
    if "intel" in gpu:
        facts.GPU = "Intel"
    elif "amd" in gpu:
        facts.GPU = "AMD"
    elif "nvidia" in gpu:
        facts.GPU = "Nvidia"
    else:
        facts.GPU = "Unknown"

    # Determine if the computer is PC or a Laptop #
    if not os.path.exists("/proc/acpi/button/lid"):
        facts.PC = "Desktop"
    else:
        facts.PC = "Laptop"

if __name__ == "__main__":
    main()
