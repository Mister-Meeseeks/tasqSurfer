#!/usr/bin/python

import os

def revisionControlInit (initPath):
    gitExec("init " + initPath)

def revisionControlAdd (addPath):
    gitExec("add " + addPath)

def revisionControlCommit (commitMsg):
    escapedMsg = commitMsg.replace("\"", "\\\"")
    gitExec("commit -a -m \"%s\"" % escapedMsg)

def revisionControlCommitWords (commitMsgWords):
    revisionControlCommit(" ".join(commitMsgWords))

def revisionControlMove (source, target):
    gitExec("mv %s %s" % (source, target))

def revisionControlRm (source):
    gitExec("rm -r %s" % (source))

def revisionControlIgnore (source):
    # Doesn't do anything, but function's a nice placeholder to show
    # that we're explicitly ignoring, and not forgetting about the dir
    pass

def gitExec (gitCmd):
    shellCmd = " ".join(["git", gitCmd, ">/dev/null"])
    os.system(shellCmd)
