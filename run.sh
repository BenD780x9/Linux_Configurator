#!/bin/sh

OS=$(grep ^ID= /etc/*release | cut -d '=' -f 2)

if [  $OS == "fedora" ] ; then
    sudo dnf -y update
    sudo dnf install -y python python-pip python-pip-wheel
elif [$OS == "ubuntu"]; then
    echo "Add ubuntu install script"
fi

pip3 install -r requirements.txt
python3 configurator.py
