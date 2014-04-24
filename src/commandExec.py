#!/usr/bin/python

from inputParse import *
from revisionControl import *
from uniqueID import *
from taskAtom import *
from treeView import *
from traverse import *
from displayOutput import *

class CommandExec:
    def __init__ (self):
        self.taskIDTracker = UniqueIDTracker(formUniqueIDTaskPath())
        self.taskTree = TaskAtom(TaskPointer(formTaskTreePath()), 
                                 self.taskIDTracker)
        self.taskStage = TaskAtom(TaskPointer(formTaskStagePath()),
                                  self.taskIDTracker)
        self.treeView = TreeView(self.taskTree.taskPointer.path, \
                                     formTreeViewPath())
        self.stageView = TreeView(self.taskStage.taskPointer.path, \
                                      formStageViewPath())

    def execCommand (self, args):
        subCommand = extractSubCommand(args)
        subArgs = extractSubCommandArgs(args)
        self.execCommandArgs(subCommand, subArgs)
        self.finalizeExec(args)

    def finalizeExec (self, args):
        self.saveToStore()
        self.commitRepository(args)

    def saveToStore (self):
        self.taskIDTracker.saveToStore()
        self.treeView.saveToStore()
        self.stageView.saveToStore()

    def commitRepository (self, args):
        revisionControlAdd(retrieveRepoTaskPath())
        revisionControlAdd(retrieveRepoViewPath())
        revisionControlAdd(retrieveRepoUniqueIDPath())
        revisionControlCommitWords(args)

    def execCommandArgs (self, subCommand, subArgs):
        if (subCommand in addCommandKeywords):
            self.execAddCommand(AddCommand(subArgs))
        elif (subCommand in listCommandKeywords):
            self.execListCommand(ListCommand(subArgs))
        elif (subCommand in cdCommandKeywords):
            self.execCdCommand(CdCommand(subArgs))
        elif (subCommand in moveCommandKeywords):
            self.execMoveCommand(MoveCommand(subArgs))
        elif (subCommand in doneCommandKeywords):
            self.execDoneCommand(DoneCommand(subArgs))
        elif (subCommand in rmCommandKeywords):
            self.execRmCommand(RemoveCommand(subArgs))
        elif (subCommand in stageCommandKeywords):
            self.execStageCommand(StageCommand(subArgs))
        elif (subCommand in unstageCommandKeywords):
            self.execUnstageCommand(UnstageCommand(subArgs))
        else:
            self.raiseUnknownCommand(subCommand)

    def execAddCommand (self, addCmd):
        parentPointer = convertTargetStr(addCmd.parentTarget, self.treeView)
        taskPointer = createTaskPointerOnParent(parentPointer, addCmd.name)
        taskAtom = TaskAtom(taskPointer, self.taskIDTracker)
        addAndWriteTaskDescription(taskAtom, addCmd.descr)
        
    def execListCommand (self, listCmd):
        listPointer = convertTargetStr(listCmd.target, self.treeView)
        taskTree = traverseViewPath(self.treeView, listPointer)
        displayTree(taskTree)
        
    def execCdCommand (self, cdCmd):
        cdPointer = convertTargetStr(cdCmd.target, self.treeView)
        self.treeView.relativeLocation.changePathRepo(cdPointer)
        
    def execMoveCommand (self, moveCmd):
        sourcePtr = convertTargetStr(moveCmd.source, self.treeView)
        targetPtr = convertTargetStr(moveCmd.target, self.treeView)
        revisionControlMove(sourcePtr, targetPtr)
        self.resetForTaskInvalidation()

    def execDoneCommand (self, doneCmd):
        targetPtr = convertTargetStr(doneCmd.target, self.treeView)
        revisionControlRm(targetPtr)
        self.resetForTaskInvalidation()

    def execRmCommand (self, rmCmd):
        targetPtr = convertTargetStr(rmCmd.target, self.treeView)
        revisionControlRm(targetPtr)
        self.resetForTaskInvalidation()

    def execStageCommand (self, stageCmd):
        if (stageCmd.name == ""):
            self.execStageListCommand(stageCmd)
        else:
            self.execStageAddCommand(stageCmd)

    def execStageListCommand (self, stageCmd):
        taskTree = traverseView(self.stageView)
        displayTree(taskTree)
        
    def execStageAddCommand (self, stageCmd):
        parentPointer = convertTargetStr("", self.stageView)
        taskPointer = createTaskPointerOnParent(parentPointer, stageCmd.name)
        taskAtom = TaskAtom(taskPointer, self.taskIDTracker)
        addAndWriteTaskDescription(taskAtom, stageCmd.descr)
                
    def execUnstageCommand (self, unstageCmd):
        if (unstageCmd.treeParent == ""):
            self.execUnstageRmCommand(unstageCmd)
        else:
            self.execUnstageAddCommand(unstageCmd)

    def execUnstageRmCommand (self, unstageCmd):
        targetPtr = convertTargetStr(unstageCmd.source, self.stageView)
        self.resetForTaskInvalidation()
        revisionControlRm(targetPtr)

    def execUnstageAddCommand (self, unstageCmd):
        sourcePtr = convertTargetStr(unstageCmd.source, self.stageView)
        targetPtr = convertTargetStr(unstageCmd.treeParent, self.treeView)
        revisionControlMove(sourcePtr, targetPtr)
        self.resetForTaskInvalidation()

    def raiseUnknownCommand (self, subCommand):
        raise Exception("Uknown command type: %s" % subCommand)

    def resetForTaskInvalidation (self):
        self.treeView.userIdxView.resetIdxToPointer()
        self.stageView.userIdxView.resetIdxToPointer()
