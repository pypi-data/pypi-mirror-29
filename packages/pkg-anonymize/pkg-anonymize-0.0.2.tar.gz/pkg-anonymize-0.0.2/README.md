# Anonymize
[![PyPI version](https://badge.fury.io/py/pkg-anonymize.svg)](https://badge.fury.io/py/pkg-anonymize)

You are being watched. Private and state-sponsored organizations are monitoring and recording your online activities. Anonymize is a program that help to protect your privacy against global mass surveillance and been secure on the web.

## Installation

### PyPI
You can install it from the Python Package Index with the pip command. This is the recommended way to install Anonymize.
``` sh
sudo pip install pkg-anonymize
```

### Source 
First, you need to have the python setuptools package installed and to get the latest source code by cloning the git repository with this command.
``` sh
git clone https://github.com/lognoz/anonymize.git
```
Finally, change to the `anonymize` directory that was just created, then run the install as root.
``` sh
sudo python setup.py install
```

## Service
To start anonymize on boot, you can run this command as root.
``` sh
systemctl enable anonymize.service
```
Make sure to already define you anonymizing preferences.
``` sh
anonymize init
```
## Usage
### Hostname
You can change your computer hostname to be sure that no network will collect your information. To generate a random one, you can run the command by writing `random` as argument.
``` sh
anonymize set hostname new-hostname
```

### Virtual Private Network
To start a connection with a virtual private network, you can send a .ovpn file or a directory to select a random one. Make sure to define `auth-user-pass` in it.
``` sh
anonymize set virtual-private-network /etc/virtual_private_network/
```

### Mac Address
To change your Mac address, you can run this command as root. Specify interface as argument. If you're not sure which one is active, you can let it blank.
``` sh
anonymize set mac-address eth0
```
