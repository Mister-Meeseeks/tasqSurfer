#!/usr/bin/python

import os

def lookupRepoPath():
    defaultRepoPath = "~/.tasqSurfer"
    repoPathEnvVarName = "TASQ_SURER_REPO"
    repoPathSet = os.getenv(repoPathEnvVarName, defaultRepoPath)
    return os.path.expanduser(repoPathSet)

def changeDirToRepo():
    changeDirToRepo(lookupRepoPath())

def changeDirToRepo (repoPath):
    if (not os.path.isdir(repoPath)):
        initAndCdRepoDir(repoPath)
    else:
        cdExtantRepoDir(repoPath)

def ddExtrantRepoDir (repoPath):
    os.chdir(repoPath)

def initAndCdRepoDir (repoPath):
    initRepoRevision(repoPath)
    cdExtrantRepoDir(repoPath)
    initRepoDirs()

def initRepoRevision (repoPath):
    revisionControlInit(repoPath)

def initRepoDirs (revisionController):
    createRepoDirs()
    commitRepoDirs()

def createRepoDirs():
    initTaskDir()
    initViewDir()
    initUniqueDir()

def commitRepoDirs (revisionController):
    revisionControlAdd(".")
    revisionController.commit("Initialization")    

def initTaskDir():
    taskDir = retrieveRepoTaskPath()
    createPointerOnDisk(formTaskTreePath(taskDir))
    createPointerOnDisk(formTaskStagePath(taskDir))

def initViewDir():
    viewDir = retrieveRepoViewPath()
    TreeView().writeToStore(formTreeViewPath(viewDir))
    TreeView().writeToStore(formStageTreeViewPath(viewDir))

def initUniqueDir():
    uniqueDir = retrieveRepoUniqueIDPath()
    uniqueIDTracker().writeToStore(formTaskIDPath(uniqueDir))
