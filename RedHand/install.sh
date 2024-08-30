#!/bin/bash
if ! [$UID == 0 ]
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
echo $repo_root
fi