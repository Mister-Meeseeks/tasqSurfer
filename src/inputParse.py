#!/usr/bin/python

from optparse import OptionParser

def extractSubCommand (args):
    return extractSpecSubCommand(args) \
        if hasSpecSubCommand(args) \
        else emptySubCommand(args)

def emptySubCommand (args):
    return (defaultKeyword, [])

def extractSpecSubCommand (args):
    isFirstFlag = args[1][0] == '-'
    return (defaultKeyword, args[1:]) if \
        isFirstFlag else (args[1], args[2:])

def hasSpecSubCommand (args):
    return len(args) > 1

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
defaultKeyword = listCommandKeywords[1]

class FlagParser:
    def __init__ (self, cmdWords):
        (opts, self.cmdWords) = self.parseFlags(cmdWords)
        self.convertOpts(opts)

    def parseFlags (self, cmdWords):
        parser = OptionParser()
        parser.add_option("--parentTask", "-p", default="")
        parser.add_option("--all", "-a",action="store_true", default=False)
        parser.add_option("--skeleton", "-s",action="store_true", default=False)
        parser.add_option("--directory", "-d",action="store_true",default=False)
        parser.add_option("--active", "-j",action="store_true", default=False)
        parser.add_option("--immediate","-i",action="store_true", default=False)
        parser.add_option("--essential","-e",action="store_true", default=False)
        parser.add_option("--activeOff", "-J", 
                          action="store_true", default=False)
        parser.add_option("--immediateOff","-I",
                          action="store_true", default=False)
        parser.add_option("--essentialOff","-E",
                          action="store_true", default=False)
        return parser.parse_args(cmdWords)

    def convertOpts (self, opts):
        self.parentTask = opts.parentTask
        self.all = opts.all
        self.skeleton = opts.skeleton or opts.directory
        self.active = self.logicalConv(opts.active, opts.activeOff)
        self.immediate = self.logicalConv(opts.immediate, opts.immediateOff)
        self.essential = self.logicalConv(opts.essential, opts.essentialOff, \
                                              not self.skeleton)

    def logicalConv (self, onArg, offArg, dflt=False):
        return self.logicalDflt(onArg, offArg) \
            if dflt else self.logicalOff(onArg, offArg)
    def logicalDflt (self, onArg, offArg):
        return onArg or (not offArg)
    def logicalOff (self, onArg, offArg):
        return onArg and (not offArg)

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

class StageCommand (FlagParser):
    def __init__ (self, cmdWords):
        FlagParser.__init__(self, cmdWords)
        self.name = self.cmdWords[0] if len(self.cmdWords) > 0 else ""
        self.descr = self.cmdWords[1] if len(self.cmdWords) > 1 else ""

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

def isHistoryStepStr (historyStr):
    return len(historyStr) > 0 and \
        (historyStr[0] == '+' or historyStr[0] == '-')

def convertHistoryStr (historyStr):
    return convertNumericHistoryStr(historyStr) \
        if isNumericHistoryStr(historyStr) else \
        convertIterHistoryStr(historyStr)

def convertNumericHistoryStr (historyStr):
    numSteps = int(historyStr[1:])
    stepDir = 1 if historyStr[0] == '+' else -1
    return stepDir * numSteps

def convertIterHistoryStr (historyStr):
    numSteps = len(historyStr)
    stepDir = 1 if historyStr[0] == '+' else -1
    return stepDir * numSteps

def isNumericHistoryStr (historyStr):
    return (len(historyStr) > 1) and \
        (not (historyStr[1] in ['+','-']))
