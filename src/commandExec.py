#!/usr/bin/python

from inputParse import *
from uniqueID import *
from taskAtom import *
from treeView import *
from traverse import *

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
            self.execRmCommand(RmCommand(subArgs))
        elif (subCommand in stageCommandKeywords):
            self.execStageCommand(StageCommand(subArgs))
        elif (subCommand in unstageCommandKeywords):
            self.execUnstageCommand(UnstageCommand(subArgs))
        else:
            self.raiseUnknownCommand(subCommand)

    def execAddCommand (self, addCmd):
        parentPointer = convertTargetStr(addCmd.parentTareget, self.treeView)
        taskAtom = createTaskPointerOnParent(parentPointer, addCmd.name)
        addAndWriteTaskDescription(taskAtom, addCmd.descr)
        revisionControlAdd(taskAtom.taskPointer.path)

    def execListCommand (self, listCmd):
        listPointer = convertTargetStr(listCmd.target, self.treeView)
        taskTree = traverseViewChild(self.treeView, listPointer)
        displayTree(taskTree)
        
    def execCdCommand (self, cdCmd):
        cdPointer = convertTargetStr(cdCmd.target, self.treeView)
        self.treeView.relativePath.changePath(cdPointer)
        
    def execMoveCommand (self, moveCmd):
        sourcePtr = convertTargetStr(moveCmd.source, self.treeView)
        targetPtr = convertTargetStr(moveCmd.target, self.treeView)
        revisionControlMove(sourcePtr.path, targetPtr.path)

    def execDoneCommand (self, doneCmd):
        sourcePtr = convertTargetStr(doneCmd.source, self.treeView)
        revisionControlRm(sourcePtr.path)

    def execRmCommand (self, rmCmd):
        sourcePtr = convertTargetStrToPointer(rmCmd.source, self.treeView)
        revisionControlRm(sourcePtr.path)

    def execStageCommand (self, stageCmd):
        if (stageCmd.name == ""):
            self.execStageListCommand(stageCmd)
        else:
            sel.execStageAddCommand(stageCmd)

    def execStageListCommand (self, stageCmd):
        taskTree = traverseView(self.stageView)
        displayTree(taskTree)
        
    def execStageAddCommand (self, stageCmd):
        tqaskPointer = createTaskPointerOnParent(self.taskTree, addCmd.name)
        taskAtom = TaskAtom(taskPointer, self.taskIDTracker)
        addAndWriteTaskDescription(taskAtom, addCmd.descr)
        revisionControlAdd(taskAtom.taskPointer.path)
        
    def execUnstageCommand (self, unstageCmd):
        if (unstageCmd.treeParentPointer == ""):
            self.execUnstageRmCommand(unstageCmd)
        else:
            self.execUnstageAddCommand(unstageCmd)

    def execUnstageRmCommand (self, unstageCmd):
        sourcePtr = convertTargetStr(unstageCmd.source, self.stageView)
        revisionControlRm(sourcePtr.path)    

    def execUnstageAddCommand (self, unstageCmd):
        sourcePtr = convertTargetStr(unstageCmd.source, self.stageView)
        targetPtr = convertTargetStr(unstageCmd.target, self.treeView)
        revisionControlMv(sourcePtr.path, targetPtr.path)

    def raiseUnknownCommand (self, subCommand):
        raise Exception("Uknown command type: %s" % subCommand)
