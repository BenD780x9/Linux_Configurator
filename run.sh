#!/bin/sh

OS=$(grep ^ID= /etc/*release | cut -d '=' -f 2)

if [  $OS == "fedora" ] ; then
    sudo dnf -y update
    sudo dnf install -y python python-pip python-pip-wheel
elif [  $OS = "ubuntu" ] ; then
# string comparison on ubuntu's sh (dash) and on posix
# is a single "=" even though bash supports "=="
# alternativly use #!/bin/bash
# consider changing the fedora comparison
    sudo apt update
    sudo apt -y upgrade
    sudo apt install python3 python3-pip
fi

pip3 install -r requirements.txt
python3 configurator.py