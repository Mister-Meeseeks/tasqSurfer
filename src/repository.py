#!/usr/bin/python

import os
from dirLayout import *
from revisionControl import *
from taskAtom import *

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

def cdExtantRepoDir (repoPath):
    os.chdir(repoPath)

def initAndCdRepoDir (repoPath):
    initRepoRevision(repoPath)
    cdExtantRepoDir(repoPath)

def initRepoRevision (repoPath):
    revisionControlInit(repoPath)
