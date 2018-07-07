class FileNode():
    def __init__(self, title, isFolder=False, expand=False):
        self.title = title
        if isFolder:
            self.children = []
            self.expand = expand
    
    def append(self, item):
        self.children.append(item)
    