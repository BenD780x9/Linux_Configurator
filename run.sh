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
    echo "Add ubuntu install script"
fi

pip3 install -r requirements.txt
python3 configurator.py
