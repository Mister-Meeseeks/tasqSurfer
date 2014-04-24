#!/usr/bin/python

import os

repoTopDir = "."
taskSubDir = "task/"
viewSubDir = "view/"
treeSubDir = "tree/"
stageSubDir = "stage/"
uniqueIDSubDir = "uniqueID/"

def retrieveRepoTaskPath():
    return retrieveSubDirectory(repoTopDir, taskSubDir)
def retrieveRepoViewPath():
    return retrieveSubDirectory(repoTopDir, viewSubDir)
def retrieveRepoUniqueIDPath():
    return retrieveSubDirectory(repoTopDir, uniqueIDSubDir)

def formTreeViewPath():
    repoViewDir = retrieveRepoViewPath()
    return formSubDirectory(repoViewDir, treeSubDir)
def formStageViewPath():
    repoViewDir = retrieveRepoViewPath()
    return formSubDirectory(repoViewDir, stageSubDir)
def formTaskTreePath():
    repoTaskDir = retrieveRepoTaskPath()
    return formSubDirectory(repoTaskDir, treeSubDir)
def formTaskStagePath():
    repoTaskDir = retrieveRepoTaskPath()
    return formSubDirectory(repoTaskDir, stageSubDir)
def formUniqueIDTaskPath():
    repoUniqueIDDir = retrieveRepoUniqueIDPath()
    return formSubDirectory(repoUniqueIDDir, taskSubDir)

def formNextIDPath (uniqueIDPath):
    return formFilePath(uniqueIDPath, "nextID.attr")
def formTaskIDPath (taskPath):
    return formFilePath(taskPath, "taskID.attr")
def formTaskDescriptionPath (taskPath):
    return formFilePath(taskPath, "description.attr")
def formTaskCreateDatePath (taskPath):
    return formFilePath(taskPath, "createDate.attr")
def formTaskBlockPath (taskPath):
    return formFilePath(taskPath, "block.attr")
def formUserIdxViewPath (viewPath):
    return formSubDirectory(viewPath, "userIdx")
def formRelativeLocationPath (viewPath):
    return formSubDirectory(viewPath, "relLoc")
def formUserIdxToPointerPath (userIdxPath):
    return formFilePath(userIdxPath, "pointerMap")
def formSubLocationPath (relPath):
    return formFilePath(relPath, "subLoc")

def retrieveSubDirectory (parentDir, subDir):
    fullDir = formSubDirectory(parentDir, subDir)
    createDirectoryIfNeeded(fullDir)
    return fullDir

def formSubDirectory (parentDir, subDir):
    return parentDir + "/" + subDir + "/"

def createDirectoryIfNeeded (fullDir):
    if (not os.path.isdir(fullDir)):
        os.mkdir(fullDir)

def formFilePath (parentDir, fileName):
    return parentDir + "/" + fileName

def fileExists (filePath):
    return os.path.isfile(filePath)

def pullDirectories (parentDir):
    listEntries = os.listdir(parentDir)
    fullListPath = map(lambda x: formSubDirectory(parentDir, x), listEntries)
    return filter(os.path.isdir, fullListPath)
