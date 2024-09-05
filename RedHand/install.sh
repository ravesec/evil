#!/bin/bash
if ! [ $UID == 0 ]
then
echo "Must be run as root."
fi
if [ $UID == 0 ]
then
apt-get update && apt-get install -y python3 
apt-get update && apt-get install -y pip
pip install paramiko
pip install file
repo_root=$(git rev-parse --show-toplevel)
mv $repo_root/RedHand/main.py /bin/rh
mkdir /lib/RedHand
touch /lib/RedHand/network.conf
touch /lib/RedHand/record.stor
mv $repo_root/RedHand/legend.list /lib/RedHand/legend.list
mv /$repo_root/RedHand/version /lib/RedHand/version
rm $0
fi