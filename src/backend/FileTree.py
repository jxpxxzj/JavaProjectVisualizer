import os
import os.path

from FileNode import FileNode

def GetFileTree(directory, rootName='/'):
    treeRoot = FileNode(rootName, isFolder=True)

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
                newNode = FileNode(lists, isFolder=False)
                treeRoot.append(newNode)

    travelFolder(treeRoot, directory)

    return treeRoot