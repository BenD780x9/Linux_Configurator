#!/bin/sh

OS=$(uname -n)

if [  $OS == "fedora" ] ; then
    sudo dnf -y update
    sudo dnf install -y python python-pip python-pip-wheel
    pip3 install -r requirements.txt
    python3 configurator.py
fi

if [  $OS == "ubuntu" ] ; then
    echo "Add ubuntu install script"
    pip3 install -r requirements.txt
    python3 configurator.py
fi

