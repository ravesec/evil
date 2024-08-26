#!/bin/bash
apt-get update && apt-get install -y python3 
apt-get update && apt-get install -y pip
apt-get update && apt-get install -y git
pip install paramiko
pip install os
pip install sys
pip install file
if ! [ -d /etc/horror ]
then
git clone https://github.com/ravesec/horror /etc/horror
fi
mv /etc/horror/ven0m/server.py /bin/venom
chmod +x /bin/venom
mv /etc/horror/ven0m/client.py /etc/venomClient
mv /etc/horror/ven0m/installer.sh /etc/venomInstaller