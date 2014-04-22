#!/usr/bin/python

import os

repoTopDir = "."
taskSubDir = "task/"
viewSubDir = "view/"
treeSubDir = "tree/"
stageSubDir = "stage/"

def retrieveRepoTaskPath():
    return retrieveSubDirectory(repoTopDir, taskSubDir)

def retrieveRepoViewPath():
    return retrieveSubDirectory(repoTopDir, viewSubDir)

def retrieveTreeViewPath():
    repoViewDir = retrieveRepoViewPath()
    return retrieveSubDirectory(repoViewDir, treeSubDir)

def retrieveStageViewPath():
    repoViewDir = retrieveRepoViewPath()
    return retrieveSubDirectory(repoViewDir, stageSubDir)

def retrieveTaskTreePath():
    repoTaskDir = retrieveRepoTaskPath()
    return retrieveSubDirectory(repoTaskDir, treeSubDir)

def retrieveTaskStagePath():
    repoTaskDir = retrieveRepoTaskPath()
    return retrieveSubDirectory(repoTaskDir, stageSubDir)

def retrieveSubDirectory (parentDir, subDir):
    fullDir = formSubDirectory(parentDir, subDir)
    createDirectoryIfNeeded(fullDir)
    return fullDir

def formSubDirectory (parentDir, subDir):
    return parentDir + "/" + subDir

def createDirectoryIfNeeded (fullDir):
    if (not os.path.isdir(fullDir)):
        os.mkdir(fullDir)


