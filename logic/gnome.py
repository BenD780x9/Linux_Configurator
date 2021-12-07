
import helper
import dnf
from facts import Facts


@staticmethod
def config_gnome():

    Message = print("Configure Gnome")
    # Enable “Click to Minimize”.
    helper.run_cmd("gsettings set org.gnome.shell.extensions.dash-to-dock click-action 'minimize'")

    # Move ‘Show Applications’ (9 dots icon) to the top.
    helper.run_cmd("gsettings set org.gnome.shell.extensions.dash-to-dock show-apps-at-top true")

    # Shorten the panel to make it compact.
    helper.run_cmd("gsettings set org.gnome.shell.extensions.dash-to-dock extend-height false")

    # Move dock to the bottom, though you may do it via System Settings.
    helper.run_cmd("gsettings set org.gnome.shell.extensions.dash-to-dock dock-position BOTTOM")

    # Enable Gnome Extensions Support.
    dnf.Dnf.install("chrome-gnome-shell", "gnome-shell-extension-prefs", "gnome-tweaks")

    # Install Gnome Weather.
    dnf.Dnf.install("gnome-weather")

    if Facts.OS == "Fedora":
        pass
    elif Facts.OS == "Ubuntu":
        pass