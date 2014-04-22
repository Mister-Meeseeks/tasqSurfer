#!/usr/bin/python

def revisionControlInit (initPath):
    os.system("git init " + initPath)

def revisionControlAdd (addPath):
    os.system("git add " + addPath)

def revisionControlCommit (commitMsg):
    os.system("git commit -a -m " + commitMsg)

