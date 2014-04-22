#!/usr/bin/python

import os

def revisionControlInit (initPath):
    os.system("git init " + initPath)

def revisionControlAdd (addPath):
    os.system("git add " + addPath)

def revisionControlCommit (commitMsg):
    escapedMsg = commitMsg.replace("\"", "\\\"")
    os.system("git commit -a -m \"%s\"" % escapedMsg)

def revisionControlCommitWords (commitMsgWords):
    revisionControlCommit(" ".join(commitMsgWords))

def revisionControlMove (source, target):
    os.system("git mv %s %s" % (source, target))

def revisionControlRm (source):
    os.system("git rm %s %s" % (source))
