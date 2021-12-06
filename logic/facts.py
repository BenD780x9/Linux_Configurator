import os
from pathlib import Path

from logic.apt import Apt
from logic.dnf import Dnf


class Facts:
    def __init__(self):
        self.HOME = None
        self.PC = None
        self.DE = None
        self.GPU = None
        self.package_manager = None

    def collect_facts(self):
        self.HOME = str(Path.home())

        # Determine the Distro and Desktop Enviroment #
        distro = os.popen("cat /etc/*release").read()
        if "fedora" in distro:
            self.package_manager = Dnf()
        elif "ubuntu" in distro:
            self.package_manager = Apt()

        if "KDE" in distro:
            self.DE = "KDE"
        else:
            self.DE = "GNOME"

        # Determine which GPU is in the PC #
        gpu = os.popen("lspci | grep VGA").read().lower()
        if "intel" in gpu:
            self.GPU = "Intel"
        elif "amd" in gpu:
            self.GPU = "AMD"
        elif "nvidia" in gpu:
            self.GPU = "Nvidia"
        else:
            self.GPU = "Unknown"

        # Determine if the computer is PC or a Laptop #
        if not os.path.exists("/proc/acpi/button/lid"):
            self.PC = "Desktop"
        else:
            self.PC = "Laptop"
