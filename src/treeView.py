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
        self.userIdxToPointer = FileStoreDict\
            (formUserIdxToPointerPath(self.path), {}, int)
        self.nextUserIdx = self.deriveNextUserIdx(self.userIdxToPointer.value)

    def resetIdxToPointer (self):
        self.userIdxToPointer.value = {}
        self.nextUserIdx = self.deriveNextUserIdx(self.userIdxToPointer.value)

    def addTaskPointer (self, taskPointer):
        lastUserIdx = self.nextUserIdx
        self.userIdxToPointer.value[self.nextUserIdx] = taskPointer
        self.nextUserIdx = self.nextUserIdx + 1
        return lastUserIdx

    def deriveNextUserIdx (self, userIdxToPointer):
        maxUserIdx = -1
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
        self.backSubLocation = FileStoreList(formBackSubLocationPath(storePath))
        self.fwdSubLocation = FileStoreList(formFwdSubLocationPath(storePath))
        self.maxHistorySize = 100

    def saveToStore (self):
        self.subLocationPath.saveToStore()
        self.backSubLocation.saveToStore()
        self.fwdSubLocation.saveToStore()

    def getTreeLocation (self, childPath=""):
        return self.cleanPath(self.getPathOnBase(childPath, ""))

    def getTreeLocationRepo (self, repoPath):
        viewPath = self.convertRepoPathToView(repoPath)
        return self.getTreeLocation(viewPath)

    def getFullPath (self):
        return self.getPathOnBase("", self.baseLocationPath)

    def getFullChild (self, childPath):
        return self.getPathOnBase(childPath, self.baseLocationPath)

    def getPathOnBase (self, childPath, basePath):
        return self.getAbsoluteOnBase(childPath, basePath) \
            if self.isAbsolutePath(childPath) else \
            self.getRelativeOnBase(childPath, basePath)

    def getAbsoluteOnBase (self, childPath, basePath):
        return self.appendPath(basePath, childPath)

    def getRelativeOnBase (self, childPath, basePath):
        subPath = self.appendPath(self.subLocationPath.value, childPath)
        return self.appendPath(basePath, subPath)

    def changePathRepo (self, pathStr):
        self.changePathView(self.convertRepoPathToView(pathStr))

    def convertRepoPathToView (self, pathStr):
        baseIdx = len(self.baseLocationPath)
        if (pathStr[:baseIdx] == self.baseLocationPath):
            return pathStr[baseIdx:]
        else:
            raise Exception("Change path target %s not in view's tree" % pathStr)

    def changePathView (self, pathStr):
        self.stepNewHistory(self.deriveTargetSubLocation(pathStr))

    def deriveTargetSubLocation (self, pathStr):
        targetPath = self.formTargetPath(pathStr)
        return self.cleanPath(targetPath)        

    def formTargetPath (self, pathStr):
        return pathStr if self.isAbsolutePath(pathStr) \
            else self.appendPath(self.subLocationPath.value, pathStr)

    def isAbsolutePath (self, pathStr):
        return len(pathStr) > 0 and pathStr[0] == "/"

    def appendPath (self, leftPath, rightPath):
        return leftPath + "/" + rightPath

    def cleanPath (self, pathStr):
        pathFields = pathStr.split("/")
        pathFields[1:] = filter(lambda x: len(x) > 0, pathFields[1:])
        pathFields = filter(lambda x: x != ".", pathFields)
        pathFields = reduce(lambda x,y: x[:-1] if y == ".." else x + [y], 
                            pathFields, [])
        pathClean = "/".join(pathFields)
        isRootClean = len(pathClean) > 0 or len(pathStr) == 0
        return pathClean if isRootClean else "/"

    def stepNewHistory (self, newLocation):
        self.pushToBackHistory(self.subLocationPath.value)
        self.fwdSubLocation.value = []
        self.subLocationPath.value = newLocation

    def stepBackHistory (self):
        if (len(self.backSubLocation) > 0):
            self.pushToFwdHistory(self.subLocationPath.value)
            self.subLocationPath.value = self.popFromBackHistory()
        
    def stepFwdHistory (self):
        if (len(self.fwdSubLocation) > 0):
            self.pushToBackHistory(self.subLocationPath.value)
            self.subLocationPath = popFromFwdHistory()

    def stepNHistory (self, nSteps):
        for i in range(abs(nSteps)):
            if (nSteps > 0):
                self.stepFwdHistory()
            else:
                self.stepBackHistory()

    def pushToBackHistory (self, subLocation):
        self.backSubLocation.value.append(subLocation)
        if (len(self.backSubLocation.value) > self.maxHistorySize):
            self.backSubLocation.value.pop(0)

    def pushToFwdHistory (self, subLoction):
        self.fwdSubLocation.value.append(subLocation)

    def popFromBackHistory (self):
        self.popFromHistory(self,backSubLocation)

    def popFromFwdHistory (self):
        self.popFromHistory(self.fwdSubLocation)

    def popFromHistory (self, historyStack):
        retVal = self.historyStack[-1]
        self.historyStack.pop(-1)
        return retVal        
