import os
import uuid
import zipfile

def UnzipFile(filePath):
    with zipfile.ZipFile(filePath,"r") as zipRef:
        randomFolder = uuid.uuid1()
        path = os.path.normpath(os.path.join(os.getcwd(), "./upload/" + str(randomFolder)))
        print(path)
        zipRef.extractall(path)
        return path
