import os
import uuid
import zipfile

def UnzipFile(filePath):
    with zipfile.ZipFile(filePath,"r") as zipRef:
        randomFolder = uuid.uuid1()
        path = os.path.normpath(os.path.join("./upload/" + str(randomFolder)))
        zipRef.extractall(path)
        return randomFolder, path
