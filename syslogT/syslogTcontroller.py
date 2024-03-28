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
    print("stdout")
    print(stdout.read().decode('utf-8'))
    print("stderr")
    print(stderr.read().decode('utf-8'))
main()