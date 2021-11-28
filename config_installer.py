from helper import *


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


def install_drivers(facts):
    if facts.OS == "Fedora":
        dnf.upgrade()
        dnf.check()
        set_hostname("fedora") # By default my machine is called localhost; hence, I rename it for better accessability on the network.

        # Enable RPM Fusion
        helper.run_cmd("rpm -Uvh http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm")
        helper.run_cmd("rpm -Uvh http://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm")
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
        helper.run_cmd("ln -s /var/lib/snapd/snap /snap") # "sudo snap refresh" AFTER REBOOT # for classic snap support
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
            helper.run_cmd("echo 'DisabledPlugins=test;invalid;uefi' | tee -a /etc/fwupd/daemon.conf") # Remove WARNING: Firmware can not be updated in legacy BIOS mode.
        helper.run_cmd("fwupdmgr get-updates")
        helper.run_cmd("fwupdmgr update")
    
    elif facts.OS == "Ubuntu":
        
        # Update system.
        Apt.update()
        Apt.upgrade()
        Apt.dist_upgrade()
        Apt.autoremove()
        Apt.autoclean()
        
        # Update disk drivers.
        helper.run_cmd("fwupdmgr get-devices")
        helper.run_cmd("fwupdmgr get-updates")
        helper.run_cmd("fwupdmgr update")
        # run_cmd("reboot now") # Nedds to save STATE if enable reboot.
        
        # System Utilities.
        Apt.install("snapd")
        Apt.install("flatpak")
        Flatpak.remote_add("flathub", "https://flathub.org/repo/flathub.flatpakrepo", "--if-not-exists")
        Flatpak.update()
        Flatpak.install("flatseal") # Tool to check or change the permissions of your flatpaks
        Apt.install("nautilus-admin")
        Apt.install("caffeine") # A little helper in case my laptop needs to stay up all night
        
        # Enable Firewall.
        run_cmd("ufw enable")
        apt.install("apt-get install gufw")
        
        # Install JAVA.
        apt.install('openjdk-14-jre')
        
        # Install Codecs and VLC.
        apt.install("libavcodec-extra", "libdvd-pkg", "ubuntu-restricted-extras", "ubuntu-restricted-addons")
        apt.install("vlc")
        apt.install("ubuntu-restricted-extras", "libdvdnav4", "gstreamer1.0-plugins-bad", "gstreamer1.0-plugins-ugly", "libdvd-pkg")
        run_cmd("dpkg-reconfigure libdvd-pkg")
        
        # Upgrade Bluetooth Codec.
        run_cmd("add-apt-repository ppa:berglh/pulseaudio-a2dp")
        run_cmd("apt update")
        apt.install("pulseaudio-modules-bt", "libldac")
        
        # Install Ubuntu Cleaner
        run_cmd("add-apt-repository ppa:gerardpuig/ppa")
        run_cmd("apt-get update")
        run_cmd("apt-get install ubuntu-cleaner")
        
    elif facts.DE == "GNOME":
    
        # Enable “Click to Minimize”.
        run_cmd("gsettings set org.gnome.shell.extensions.dash-to-dock click-action 'minimize'")
        
        # Move ‘Show Applications’ (9 dots icon) to the top.
        run_cmd("gsettings set org.gnome.shell.extensions.dash-to-dock show-apps-at-top true")
        
        # Shorten the panel to make it compact.
        run_cmd("gsettings set org.gnome.shell.extensions.dash-to-dock extend-height false")
        
        # Move dock to the bottom, though you may do it via System Settings.
        run_cmd("gsettings set org.gnome.shell.extensions.dash-to-dock dock-position BOTTOM")
        
        # Disable USB and other removable device icons from panel.
        #run_cmd("gsettings set org.gnome.shell.extensions.dash-to-dock show-mounts false")
        
        # Enable Gnome Extensions Support.
        apt.install("chrome-gnome-shell", "gnome-shell-extension-prefs", "gnome-tweaks")


        # Install Gnome Weather.
        apt.install("gnome-weather")
    
    elif facts.PC == "Laptop":
        
        if facts.OS == "Fedora":
            # Reduce Battery Usage - TLP.
            Dnf.install("tlp", "tlp-rdw")
            helper.run_cmd("systemctl enable tlp")
            
        if facts.OS == "Ubuntu":
            run_cmd("add-apt-repository ppa:linuxuprising/apps") # -y ??
            run_cmd("apt-get update")
            run_cmd("apt-get install tlp tlpui")
            run_cmd("tlp start")

def install_gpu(facts):

    if facts.GPU == "Nvidia":
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
 
def install_dropbox(facts):
    if facts.OS == "Fedora":
        dnf.install("dropbox", "nautilus-dropbox")

    elif facts.OS == "Ubuntu":
        apt.install("nautilus-dropbox")
        
def install_nextcloud(facts):
    if facts.OS == "Fedora":
        dnf.install("nextcloud-client", "nextcloud-client-nautilus")
        run_cmd("-i")
        run_cmd("echo 'fs.inotify.max_user_watches = 524288' >> /etc/sysctl.conf")
        run_cmd("sysctl -p")
        
    elif facts.OS == "Ubuntu":
        apt.install("nextcloud-desktop")
        

def install_google():
    Dnf.install("python3-devel", "python3-pip", "python3-inotify", "python3-gobject", "cairo-devel", "cairo-gobject-devel", "libappindicator-gtk3")
    helper.run_cmd("python3 -m pip install --upgrade google-api-python-client")
    helper.run_cmd("python3 -m pip install --upgrade oauth2client")
    helper.run_cmd("yum install -y overgrive-3.3.*.noarch.rpm")


def install_skype():
    Flatpak.install("skype")


def install_zoom():    
    flatpak.install("zoom")
        
def install_chrome(facts):
    if facts.OS == "Fedora":
        dnf.install("fedora-workstation-repositories")
        dnf.config_manager("set-enabled", "google-chrome")
        dnf.install("google-chrome-stable")
        
    elif facts.OS == "Ubuntu":
        download_file("https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")
        dpkg_install("google-chrome-stable_current_amd64.deb")
        
def install_chromium(facts):
    if facts.OS == "Fedora":
        dnf.install("chromium")
        
    elif facts.OS == "Ubuntu":
        apt.install("chromium-browser")
