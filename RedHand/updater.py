#!/usr/bin/env python3
import os
import file

def main():
    os.system("rm /bin/rh")
    os.system("rm /lib/RedHand/version")
    os.system("mv /tmp/github/RedHand/version /lib/RedHand/version")
    os.system("mv /tmp/github/RedHand/main.py /bin/rh")
    os.system("chmod +x /bin/rh")
main()