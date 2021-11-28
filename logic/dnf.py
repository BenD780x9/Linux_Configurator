import subprocess

import helper
from logic.flatpak import Flatpak


class Dnf:
    @staticmethod
    def do(cmd):
        """run an unimplemented command"""
        helper.run_cmd(f"dnf {cmd}")

    @staticmethod
    def upgrade():
        Dnf.do("-y upgrade --refresh")

    @staticmethod
    def check():
        Dnf.do("check")

    @staticmethod
    def install(package, *args):
        cmd = f"install -y {package}"
        for arg in args:
            cmd += " " + arg
        Dnf.do(cmd)

    @staticmethod
    def group(operation, group, *args):
        cmd = f"group {operation} {group}"
        for arg in args:
            cmd += " " + arg
        Dnf.do(cmd)

    @staticmethod
    def group_update(group, *args):
        cmd = f"groupupdate {group}"
        for arg in args:
            cmd += " " + arg
        Dnf.do(cmd)

    @staticmethod
    def config_manager(operation, value):
        Dnf.do(f"config-manager --{operation} {value}")

    @staticmethod
    def install_drivers():
        Dnf.upgrade()
        Dnf.check()
        helper.set_hostname(
            "fedora")  # By default my machine is called localhost; hence, I rename it for better accessability on the network.

        # Enable RPM Fusion
        helper.run_cmd(
            "rpm -Uvh http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm")
        helper.run_cmd(
            "rpm -Uvh http://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm")
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
        helper.run_cmd("ln -s /var/lib/snapd/snap /snap")  # "sudo snap refresh" AFTER REBOOT # for classic snap support
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
            helper.run_cmd(
                "echo 'DisabledPlugins=test;invalid;uefi' | tee -a /etc/fwupd/daemon.conf")  # Remove WARNING: Firmware can not be updated in legacy BIOS mode.
        helper.run_cmd("fwupdmgr get-updates")
        helper.run_cmd("fwupdmgr update")
