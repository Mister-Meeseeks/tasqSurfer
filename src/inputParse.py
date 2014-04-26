#!/usr/bin/python

from optparse import OptionParser

def extractSubCommand (args):
    return args[1] if len(args) > 1 \
        else listCommandKeywords[0]

def extractSubCommandArgs (args):
    return args[2:]

addCommandKeywords = ["add"]
modifyCommandKeywords = ["mod", "modify"]
listCommandKeywords = ["ls", "list"]
cdCommandKeywords = ["cd"]
cdListCommandKeywords = ["cdd", "cdl"]
pwdCommandKeywords = ["pwd"]
moveCommandKeywords = ["move", "mv"]
doneCommandKeywords = ["done"]
rmCommandKeywords = ["rm", "cancel"]
stageCommandKeywords = ["stage"]
unstageCommandKeywords = ["unstage"]

class FlagParser:
    def __init__ (self, cmdWords):
        (opts, self.cmdWords) = self.parseFlags(cmdWords)
        self.convertOpts(opts)

    def parseFlags (self, cmdWords):
        parser = OptionParser()
        parser.add_option("--parentTask", "-p", default="")
        parser.add_option("--skeleton", "-s",action="store_true", default=False)
        parser.add_option("--active", "-a", action="store_true", default=False)
        parser.add_option("--immediate","-I",action="store_true", default=False)
        parser.add_option("--essential","-E",action="store_true", default=False)
        parser.add_option("--skeletonOff", action="store_true", default=False)
        parser.add_option("--activeOff", action="store_true", default=False)
        parser.add_option("--immediateOff", action="store_true", default=False)
        parser.add_option("--essentialOff", action="store_true", default=False)
        return parser.parse_args(cmdWords)

    def convertOpts (self, opts):
        self.parentTask = opts.parentTask
        self.skeleton = opts.skeleton
        self.active = opts.active
        self.immediate = opts.immediate
        self.essential = opts.essential
        self.skeletonOff = opts.skeletonOff
        self.activeOff = opts.activeOff
        self.immediateOff = opts.immediateOff
        self.essentialOff = opts.essentialOff

class AddCommand (FlagParser):
    def __init__ (self, cmdWords):
        FlagParser.__init__(self, cmdWords)
        self.parseArgs(self.cmdWords)
        
    def parseArgs (self, args):
        self.name = args[0]
        self.descr = args[1] if len(args) > 1 else ""

class ModifyCommand (FlagParser):
    def __init__ (self, cmdWords):
        FlagParser.__init__ (self, cmdWords)
        self.parseArgs(self.cmdWords)

    def parseArgs (self, args):
        self.target = args[0]
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

class ListCommand (FlagParser):
    def __init__ (self, cmdWords):
        FlagParser.__init__(self, cmdWords)
        self.target = self.cmdWords[0] if len(self.cmdWords) > 0 else ""

class CdCommand:
    def __init__ (self, cmdWords):
        self.target = cmdWords[0]

class PwdCommand:
    def __init__ (self, pwdWords):
        self.empty = None

class StageCommand:
    def __init__ (self, cmdWords):
        self.name = cmdWords[0] if len(cmdWords) > 0 else ""
        self.descr = cmdWords[1] if len(cmdWords) > 1 else ""

class UnstageCommand:
    def __init__ (self, cmdWords):
        self.source = cmdWords[0]
        self.treeParent = cmdWords[1] if len(cmdWords) > 1 else ""

def convertTargetStr (targetStr, treeView):
    return convertTargetIdxStrToPointer(targetStr, treeView) \
        if isIdxTargetStr(targetStr) else \
        convertTargetPathStrToPointer(targetStr, treeView)

def convertTargetIdxStrToPointer (targetStr, treeView):
    targetIdx = int(targetStr)
    return treeView.userIdxView.userIdxToPointer.value[targetIdx]

def convertTargetPathStrToPointer (targetStr, treeView):
    return treeView.relativeLocation.getFullChild(targetStr)

def isIdxTargetStr (targetStr):
    try:
        int(targetStr)
        return True
    except ValueError:
        return False

