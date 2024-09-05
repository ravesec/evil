#!/usr/bin/env python3
import os
import time

def main():
    os.system("rm /bin/rh")
    os.system("rm /lib/RedHand/version")
    os.system("mv /tmp/github/RedHand/version /lib/RedHand/version")
    os.system("mv /tmp/github/RedHand/main.py /bin/rh")
    time.sleep(1)
    os.system("chmod +x /bin/rh")
main()