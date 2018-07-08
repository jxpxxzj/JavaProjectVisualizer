class FileNode():
    def __init__(self, title, isFolder=False, expand=False, path=None):
        self.title = title
        if isFolder:
            self.children = []
            self.expand = expand
        else:
            self.path = path
    
    def append(self, item):
        self.children.append(item)
    