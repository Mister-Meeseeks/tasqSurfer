#!/usr/bin/python

from storeFile import *
from dirLayout import *
from taskAtom import *

class TreeView (DirectoryOwner):
    def __init__ (self, treeViewRootPath, treeStoreDirPath):
        DirectoryOwner.__init__(self, treeStoreDirPath)
        self.userIdxView = UserIdxView(formUserIdxViewPath(self.path))
        self.relativeLocation = RelativeLocation\
            (treeViewRootPath, formRelativeLocationPath(self.path))

    def saveToStore (self):
        self.userIdxView.saveToStore()
        self.relativeLocation.saveToStore()

class UserIdxView (DirectoryOwner):
    def __init__ (self, userIdxViewPath):
        DirectoryOwner.__init__(self, userIdxViewPath)
        self.userIdxToPointerPath = formUserIdxToPointerPath(self.path)
        self.userIdxToPointer = FileStoreDict(self.userIdxToPointerPath, {},
                                              int, TaskPointer)
        self.nextUserIdx = self.deriveNextUserIdx(self.userIdxToPointer.value)

    def addTaskPointer (self, taskPointer):
        lastUserIdx = self.nextUserIdx
        self.userIdxToPointer[self.nextUserIdx] = taskPointer
        self.nextUserIdx = self.nextUserIdx + 1
        return lastUserIdx

    def deriveNextUserIdx (self, userIdxToPointer):
        maxUserIdx = 0
        for userIdx in userIdxToPointer:
            maxUserIdx = max(maxUserIdx, userIdx)
        return maxUserIdx+1

    def saveToStore (self):
        self.userIdxToPointer.saveToStore()

def pointerMapFromStr (mapStr):
    return pointerMapFromStrs(splitStringLines(mapStr))

def pointerMapFromStrs (mapStrs):
    retDict = {}
    for mapStr in mapStrs:
        mapFields = mapStr.split("\t")
        retDict[int(mapFields[0])] = TaskPointer(mapFields[1])
    return retDict

class RelativeLocation (DirectoryOwner):
    def __init__ (self, baseLocationPath, storePath):
        DirectoryOwner.__init__(self, storePath)
        self.baseLocationPath = baseLocationPath
        self.subLocationPath = FileStoreSingle\
            (formSubLocationPath(storePath), "/")

    def saveToStore (self):
        self.subLocationPath.saveToStore()

    def getFullPath (self):
        return self.appendPath(self.baseLocationPath, \
                                   self.subLocationPath.value)

    def getFullChild (self, childPath):
        return self.appendPath(self.getFullPath(), childPath)

    def changePath (self, pathStr):
        targetPath = self.formTargetPath(pathStr)
        self.subLocationPath.value = self.cleanPath(targetPath)

    def formTargetPath (self, pathStr):
        pathStr if self.isAbsolutePath(pathStr) \
            else self.appendPath(self.subLocationPath.value, pathStr)

    def isAbsolutePath (self, pathStr):
        return len(pathStr) == 0 or pathStr[0] == "/"

    def appendPath (self, leftPath, rightPath):
        return leftPath + "/" + rightPath

    def cleanPath (self, pathStr):
        pathFields = pathStr.split("/")
        pathFields = filter(lambda x: len(x) == 0, pathFields)
        pathFields = filter(lambda x: x == ".", pathFields)
        pathFields = reduce(lambda x,y: x[:-1] if y == ".." else x + [y])
        return pathFields
