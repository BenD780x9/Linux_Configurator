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
