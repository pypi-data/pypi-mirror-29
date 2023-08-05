# Anonymize
You are being watched. Private and state-sponsored organizations are monitoring and recording your online activities. Anonymize is a program that help to protect your privacy against global mass surveillance and been secure on the web.

## Synopsis
**anonymize** [ **subcommand** ]  [ **args** ]  [ **options** ]

## Options
**-i, init**<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Configure user preference.

**-e, exec, execute**<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Anonymize personal info with user preference.

**-h, --help, help**<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Display the help and exit.

**-v, --version**<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Print version information and exit.

**-s, --set, set [args] [options]**<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Set virtual private network, hostname or mac address

## Examples
**-V, virtual-private-network [path]**<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Connect to an ovpn file. You can send a dir path and anonymize will select a random one.<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;***Example:*** *anonymize set virtual-private-network /etc/virtual_private_network/*

**-H, hostname [hostname]**<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Change your computer hostname. You can verify you new one with cat /etc/hostname.<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;***Example:*** *anonymize set hostname new-hostname*

**-M, mac-address [interface]**<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Change your mac address on interface.<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;***Example:*** *anonymize set mac-address eth0*
