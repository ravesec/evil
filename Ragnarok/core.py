import os

def main():
    fileList = findFiles()
    
def findFiles():
    fileList = []
    for root, dirs, files in os.walk("/"):
        for file in files:
            path = os.path.join(root, file)
            fileList.append(path)
    return fileList
    
if(os.getuid() == 0):
    main()