#!/usr/bin/python

import os
from revisionControl import *

def lookupRepoPath():
    defaultRepoPath = "~/.tasqSurfer"
    repoPathEnvVarName = "TASQ_SURER_REPO"
    repoPathSet = os.getenv(repoPathEnvVarName, defaultRepoPath)
    return os.path.expanduser(repoPathSet)

def changeDirToRepo():
    changeDirToTargetRepo(lookupRepoPath())

def changeDirToTargetRepo (repoPath):
    if (not os.path.isdir(repoPath)):
        initAndCdRepoDir(repoPath)
    else:
        cdExtantRepoDir(repoPath)

def cdExtrantRepoDir (repoPath):
    os.chdir(repoPath)

def initAndCdRepoDir (repoPath):
    initRepoRevision(repoPath)
    cdExtrantRepoDir(repoPath)
    initRepoDirs()

def initRepoRevision (repoPath):
    revisionControlInit(repoPath)

def initRepoDirs():
    createRepoDirs()
    commitRepoDirs()

def createRepoDirs():
    initTaskDir()
    initViewDir()
    initUniqueDir()

def commitRepoDirs():
    revisionControlAdd(".")
    revisionController.commit("Initialization")    

def initTaskDir():
    createPointerOnDisk(retrieveTaskTreePath())
    createPointerOnDisk(retrieveTaskStagePath())

def initViewDir():
    TreeView().writeToStore(retrieveTreeViewPath())
    TreeView().writeToStore(retrieveStageViewPath())

def initUniqueDir():
    uniqueIDTracker().writeToStore(retrieveTaskIDPath())
