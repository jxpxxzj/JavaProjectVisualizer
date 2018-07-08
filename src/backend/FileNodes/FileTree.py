import os
import os.path

from FileNodes.FileNode import FileNode

def GetFileTree(directory, rootName='/'):
    treeRoot = FileNode(rootName, isFolder=True, expand=True)

    def travelFolder(treeRoot, directory):
        files = os.listdir(directory)
        files.sort(reverse=True)
        for lists in files:
            path = os.path.join(directory, lists) 
            if os.path.isdir(path):
                newNode = FileNode(lists, isFolder=True)
                treeRoot.append(newNode)
                travelFolder(newNode, path)
            else:
                pathList = os.path.normpath(path).replace('\\', '/').split('/')[2:]
                dpath = '/'.join(pathList)
                newNode = FileNode(lists, isFolder=False, path=dpath)
                treeRoot.append(newNode)

    travelFolder(treeRoot, directory)

    return treeRoot