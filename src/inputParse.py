#!/usr/bin/python

from optparse import OptionParser

def extractSubCommand (args):
    return args[1] if len(args) > 1 \
        else listCommandKeywords[0]

def extractSubCommandArgs (args):
    return args[2:]

addCommandKeywords = ["add"]
listCommandKeywords = ["ls", "list"]
cdCommandKeywords = ["cd"]
moveCommandKeywords = ["move", "mv"]
doneCommandKeywords = ["done"]
rmCommandKeywords = ["rm", "cancel"]
stageCommandKeywords = ["stage"]
unstageCommandKeywrods = ["unstage"]

class AddCommand:
    def __init__ (self, cmdWords):
        (opts, args) = self.parseFlags(cmdWords)
        self.parseOpts(opts)
        self.parseArgs(args)

    def parseFlags (self, cmdWords):
        parser = OptionParser()
        parser.add_option("--parentTask", "-p", default=False)
        parser.parse_args(cmdWords)

    def parserOpts (self, opts):
        self.parentTarget = opt.parentTask
        
    def parseArgs (self, args):
        self.name = args[0]
        self.descr = args[1] if len(args) > 1 else ""

class MoveCommand:
    def __init__ (self, cmdWords):
        self.source = cmdWords[0]
        self.target = cmdWords[1]

class DoneCommand:
    def __init__ (self, cmdWords):
        self.target = cmdWords[0]

class RemoveCommand:
    def __init__ (self, cmdWords):
        self.target = cmdWords[0]

class ListCommand:
    def __init__ (self, cmdWords):
        self.target = cmdWords[0] if len(cmdWords) > 0 else ""

class CdCommand:
    def __init __ (self, cmdWords):
        self.target = cmdWords[0]

class StageCommand:
    def __init__ (self, cmdWords):
        self.name = args[0] if len(cmdWords) > 0 else ""
        self.descr = args[1] if len(cmdWords) > 1 else ""

class UnstageCommand:
    def __init__ (self, cmdWords):
        self.stagePointer = cmdWords[0]
        self.treeParentPointer = cmdWords[1] if len(cmdWords) > 1 else ""

def convertTargetStrToPointer (targetStr, treeView):
    return convertTargetIdxStrToPointer(targetStr, treeView) \
        if isIdxTargetStr(targetStr) else \
        convertTargetPathStrToPointer(targetStr, treeView)

def convertTargetIdxStrToPointer (targetStr, treeView):
    targetIdx = int(targetStr)
    return treeView.userIdxView.userIdxToPointer[targetIdx]

def convertTargetPathStrToPointer (targetStr, treeView):
    return treeView.relativePath.getFullPath(targetStr)

def isIdxTargetStr (targetStr):
    try:
        int(s)
        return True
    except ValueError:
        return False
        