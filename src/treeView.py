#!/usr/bin/python

class TreeView:
    def __init__ (self):
        self.userIdxView = UserIdxView()
        self.relativePath = RelativePathLocate()

    def __init__ (self, treeStoreDir):
        userIdxPathStore = formUserIdxStore(treeStoreDir)
        relativePathStore = formRelativePathStore(treeStoreDir)
        self.userIdxView = UserIdxView(userIdxPathStore)
        self.relativePath = RelativePathLocate(relativePathStore)

    def writeToStore (self, treeStoreDir):
        self.userIdxView.writeToStore(treeStoreDir)
        self.relativePath.writeToStore(treeStoreDir)

class UserIdxView:
    def __init__ (self):
        self.nextUserIdx = 0
        self.userIdxToPointer = {}

    def __init__ (self, userIdxPath):
        self.nextUserIdx = 0
        for line in open(userIdxPath, 'r').readlines():
            fields = line.split(",")
            self.addPreSpecMapping(int(fields[0]), fields[1])

    def addPreSpecMapping (self, userIdx, taskPath):
        self.userIdxToPointer[userIdx] = TaskPointer(taskPath)
        self.nextUserIdx = max(self.nextUserIdx, userIdx)

    def addTaskPointer (self, taskPointer):
        lastUserIdx = self.nextUserIdx
        self.userIdxToPointer[self.nextUserIdx] = taskPointer
        self.nextUserIdx = self.nextUserIdx + 1
        return lastUserIdx

    def writeToStore (self, outPath):
        mapStream = open(outPath, 'w')
        for userIdx in self.userIdxToPointer:
            taskPointer = self.userIdxToPointer[userIdx]
            print >> mapStream, "%d,%s" % (userIdx, taskPointer.path)

class RelativePathLocate:
    def __init__ (self):
        self.basePath = None
        self.subPath = "/"

    def __init__ (self, storePath):
        storeStream = open(storePath, 'r')
        self.basePath = storeStream.readline()
        self.subPath = storeStream.readline()

    def writeToStore (self, storePath):
        storeStream = open(storePath, 'w')
        print >> storeStream, self.basePath
        print >> storeStream, self.subPath

    def setBasePath (self, basePath):
        self.basePath = basePath

    def getFullPath (self):
        return self.appendPath(self.basePath, self.subPath)

    def getFullChild (self, childPath):
        return self.appendPath(self.getFullPath(), childPath)

    def changePath (self, pathStr):
        targetPath = self.formTargetPath(pathStr)
        self.subPath = self.cleanPath(targetPath)

    def formTargetPath (self, pathStr):
        pathStr if self.isAbsolutePath(pathStr) \
            else self.appendPath(self.subPath, pathStr)

    def isAbsolutePath (self, pathStr):
        return len(pathStr) == 0 or pathStr[0] == "/"

    def appendPath (self, leftPath, rightPath):
        return self.leftPath + "/" + self.rightPath

    def cleanPath (self, pathStr):
        pathFields = pathStr.split("/")
        pathFields = filter(lambda x: len(x) == 0, pathFields)
        pathFields = filter(lambda x: x == ".", pathFields)
        pathFields = reduce(lambda x,y: x[:-1] if y == ".." else x + [y])
        return pathFields

def createTreeViewOnDisk (viewBaseDir, storeDir):
    createTreeViewDirOnDisk(storeDir)
    treeView = createTreeViewInst(viewBaseDir)
    treeView.writeToStore(storeDir)
    return treeView

def createTreeViewInst (viewBaseDir):
    treeView = TreeView()
    treeView.relativePath.setBasePath(viewBaseDir)
    return treeView

def createTreeViewDirOnDisk (storeDir):
    makeDirectory(storeDir)
