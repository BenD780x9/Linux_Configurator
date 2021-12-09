from helper import run_cmd
from logic.flatpak import Flatpak
import sys
#from logic.facts import Facts

Message = ""

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
        
        sys.stdout.write("Intsalling drivers...")
        # Update system.
        Apt.update()
        Apt.upgrade()
        Apt.dist_upgrade()
        Apt.autoremove()
        Apt.autoclean()

        # Update disk drivers.
        sys.stdout.write("Update disk drivers")
        run_cmd("fwupdmgr get-devices")
        run_cmd("fwupdmgr get-updates")
        run_cmd("fwupdmgr update")
        # run_cmd("reboot now") # Nedds to save STATE if enable reboot.

        # System Utilities.
        sys.stdout.write("installing System Utilities")
        Apt.install("snapd")
        Apt.install("flatpak")
        Flatpak.remote_add("flathub", "https://flathub.org/repo/flathub.flatpakrepo", "--if-not-exists")
        Flatpak.update()

        # Tool to check or change the permissions of your flatpaks
        Flatpak.install("flatseal")
        Apt.install("nautilus-admin")

        # A little helper in case my laptop needs to stay up all night
        Apt.install("caffeine")

        # Enable Firewall.
        sys.stdout.write("Enable fireWall")
        run_cmd("ufw enable")
        Apt.install("gufw")

        # Install JAVA.
        sys.stdout.write("Install JAVA")
        Apt.install('openjdk-14-jre')

        # Install Codecs and VLC.
        sys.stdout.write("Installing Codecs and VLC")
        Apt.install("libavcodec-extra", "libdvd-pkg", "ubuntu-restricted-extras", "ubuntu-restricted-addons")
        Apt.install("vlc")
        Apt.install("ubuntu-restricted-extras", "libdvdnav4", "gstreamer1.0-plugins-bad", "gstreamer1.0-plugins-ugly",
                    "libdvd-pkg")
        run_cmd("dpkg-reconfigure libdvd-pkg")

        # Upgrade Bluetooth Codec.
        run_cmd("add-apt-repository ppa:berglh/pulseaudio-a2dp")
        run_cmd("apt update")
        Apt.install("pulseaudio-modules-bt", "libldac")

        # Install Ubuntu Cleaner.
        sys.stdout.write("Installing Ubuntu Cleaner")
        run_cmd("add-apt-repository ppa:gerardpuig/ppa")
        Apt.update()
        Apt.install("ubuntu-cleaner")

    @staticmethod
    def config_laptop():
        sys.stdout.write("Config Laptop stuff")
        run_cmd("add-apt-repository ppa:linuxuprising/apps")  # -y ??
        Apt.update()
        Apt.install("tlp", "tlpui")
        run_cmd("tlp start")

    @staticmethod
    def install_gpu(gpu):

        sys.stdout.write("Installing GPU drivers")

        if gpu == "Nvidia":
            run_cmd("modinfo -F version nvidia")

            # rhel/centos users can use kmod-nvidia instead
            Apt.install("akmod-nvidia")

            # optional for cuda/nvdec/nvenc support
            Apt.install("xorg-x11-drv-nvidia-cuda")
            Apt.install("xorg-x11-drv-nvidia-cuda-libs")
            Apt.install("vdpauinfo", "libva-vdpau-driver", "libva-utils")
            Apt.install("vulkan")
            run_cmd("modinfo -F version nvidia")

    @staticmethod
    def install_dropbox():
        sys.stdout.write("Installing Dropbox")
        Apt.install("nautilus-dropbox")

    @staticmethod
    def install_nextcloud():
        sys.stdout.write("Installing NextCloud")
        Apt.install("nextcloud-desktop")

    # if Facts.OS == "Fedora":
    #     pass
    # elif Facts.OS == "Ubuntu":
    #     pass    
