#!/bin/bash
if ! [$UID == "root" ]
then
echo "Must be run as root."
fi
if [ $UID == "root" ]
then
apt-get update && apt-get install -y python3 
apt-get update && apt-get install -y pip
pip install paramiko
pip install file
repo_root=$(git rev-parse --show-toplevel)
echo $repo_root
fi