from helper import run_cmd
from logic.flatpak import Flatpak


class Apt:
    @staticmethod
    def do(cmd):
        """run an unimplemented command"""
        run_cmd(f"apt {cmd}")

    @staticmethod
    def update():
        Apt.do("update")

    @staticmethod
    def upgrade():
        Apt.do("-y upgrade")

    @staticmethod
    def dist_upgrade():
        Apt.do("-y dist-upgrade")

    @staticmethod
    def autoremove():
        Apt.do("-y autoremove")

    @staticmethod
    def autoclean():
        Apt.do("-y autoclean")

    @staticmethod
    def install(package, *args):
        cmd = f"install -y {package}"
        for arg in args:
            cmd += " " + arg
        Apt.do(cmd)

    @staticmethod
    def install_drivers():
        Apt.update()
        Apt.upgrade()
        Apt.dist_upgrade()
        Apt.autoremove()
        Apt.autoclean()

        # Update disk drivers.
        run_cmd("fwupdmgr get-devices")
        run_cmd("fwupdmgr get-updates")
        run_cmd("fwupdmgr update")
        # run_cmd("reboot now") # Nedds to save STATE if enable reboot.

        # System Utilities.
        Apt.install("snapd")
        Apt.install("flatpak")
        Flatpak.remote_add("flathub", "https://flathub.org/repo/flathub.flatpakrepo", "--if-not-exists")
        Flatpak.update()
        Flatpak.install("flatseal")  # Tool to check or change the permissions of your flatpaks
        Apt.install("nautilus-admin")
        Apt.install("caffeine")  # A little helper in case my laptop needs to stay up all night

        # Install Codecs and VLC.
        Apt.install("vlc")
        Apt.install("libavcodec-extra", "libdvd-pkg")
        run_cmd("dpkg-reconfigure libdvd-pkg")
