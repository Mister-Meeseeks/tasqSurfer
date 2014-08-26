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
        elif (subCommand in modifyCommandKeywords):
            self.execModifyCommand(ModifyCommand(subArgs))
        elif (subCommand in listCommandKeywords):
            self.execListCommand(ListCommand(subArgs))
        elif (subCommand in cdCommandKeywords):
            self.execCdCommand(CdCommand(subArgs))
        elif (subCommand in cdListCommandKeywords):
            self.execCdListCommand(ListCommand(subArgs))
        elif (subCommand in pwdCommandKeywords):
            self.execPwdCommand(PwdCommand(subArgs))
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
        parentPointer = convertTargetStr(addCmd.parentTask, self.treeView)
        taskPointer = createTaskPointerOnParent(parentPointer, addCmd.name)
        taskAtom = TaskAtom(taskPointer, self.taskIDTracker)
        self.modifyTaskProperties(taskAtom.taskProperties, addCmd)
        
    def execModifyCommand (self, modCmd):
        targetPointer = convertTargetStr(modCmd.target, self.treeView)
        taskAtom = TaskAtom(TaskPointer(targetPointer), self.taskIDTracker)
        self.modifyTaskProperties(taskAtom.taskProperties, modCmd)

    def modifyTaskProperties (self, taskProperties, modCmd):
        if (modCmd.descr != ""):
            taskProperties.description.value = modCmd.descr
        if (modCmd.skeleton):
            taskProperties.blocks.value.skeleton = True
        elif (modCmd.skeletonOff):
            taskProperties.blocks.value.skeleton = False
        if (modCmd.active):
            taskProperties.blocks.value.active = True
        elif (modCmd.activeOff):
            taskProperties.blocks.value.active = False
        if (modCmd.immediate):
            taskProperties.blocks.value.immediate = True
        elif (modCmd.immediateOff):
            taskProperties.blocks.value.immediate = False
        if (modCmd.essential):
            taskProperties.blocks.value.essential = True
        elif (modCmd.essentialOff):
            taskProperties.blocks.value.essential = False
        else:
            taskProperties.blocks.value.essential = True
        taskProperties.saveToStore()

    def execListCommand (self, listCmd):
        listPointer = convertTargetStr(listCmd.target, self.treeView)
        taskTree = self.filterTreeForCommand(\
            traverseViewPath(self.treeView, listPointer), listCmd)
        displayTree(self.treeView, taskTree)
        
    def filterTreeForCommand (self, tree, listCmd):
        if (not listCmd.skeleton):
            filterTaskTree(lambda a: not getTaskBlocks(a).skeleton, tree)
        if (listCmd.active):
            filterTaskTree(lambda a: getTaskBlocks(a).active, tree)
        if (listCmd.immediate):
            filterTaskTree(lambda a: getTaskBlocks(a).immediate,tree)
        if (listCmd.essential):
            filterTaskTree(lambda a: getTaskBlocks(a).essential,tree)
        return tree

    def execCdCommand (self, cdCmd):
        if (isHistoryStepStr(cdCmd.target)):
            self.execCdHistoryCommand(cdCmd)
        else:
            self.execCdTargetCommand(cdCmd)

    def execCdHistoryCommand (self, cdCmd):
        histSteps = convertHistoryStr(cdCmd.target)
        self.treeView.relativeLocation.stepNHistory(histSteps)
        printRelativeLocation(self.treeView)

    def execCdTargetCommand (self, cdCmd):
        cdPointer = convertTargetStr(cdCmd.target, self.treeView)
        self.treeView.relativeLocation.changePathRepo(cdPointer)

    def execCdListCommand (self, listCmd):
        self.execCdCommand(listCmd)
        self.sanitizeListPostCd(listCmd)
        self.execListCommand(listCmd)

    def sanitizeListPostCd (self, listCmd):
        listCmd.target = ""

    def execPwdCommand (self, pwdCmd):
        printRelativeLocation(self.treeView)
                        
    def execMoveCommand (self, moveCmd):
        sourcePtr = convertTargetStr(moveCmd.source, self.treeView)
        targetPtr = convertTargetStr(moveCmd.target, self.treeView)
        revisionControlMove(sourcePtr, targetPtr)

    def execDoneCommand (self, doneCmd):
        targetPtr = convertTargetStr(doneCmd.target, self.treeView)
        revisionControlRm(targetPtr)

    def execRmCommand (self, rmCmd):
        targetPtr = convertTargetStr(rmCmd.target, self.treeView)
        revisionControlRm(targetPtr)

    def execStageCommand (self, stageCmd):
        if (stageCmd.name == ""):
            self.execStageListCommand(stageCmd)
        else:
            self.execStageAddCommand(stageCmd)

    def execStageListCommand (self, stageCmd):
        taskTree = traverseView(self.stageView)
        displayTreeTraverse(taskTree)
        
    def execStageAddCommand (self, stageCmd):
        parentPointer = convertTargetStr("", self.stageView)
        taskPointer = createTaskPointerOnParent(parentPointer, stageCmd.name)
        taskAtom = TaskAtom(taskPointer, self.taskIDTracker)
        self.modifyTaskProperties(taskAtom.taskProperties, stageCmd)
        
                
    def execUnstageCommand (self, unstageCmd):
        if (unstageCmd.treeParent == ""):
            self.execUnstageRmCommand(unstageCmd)
        else:
            self.execUnstageAddCommand(unstageCmd)

    def execUnstageRmCommand (self, unstageCmd):
        targetPtr = convertTargetStr(unstageCmd.source, self.stageView)
        revisionControlRm(targetPtr)

    def execUnstageAddCommand (self, unstageCmd):
        sourcePtr = convertTargetStr(unstageCmd.source, self.stageView)
        targetPtr = convertTargetStr(unstageCmd.treeParent, self.treeView)
        revisionControlMove(sourcePtr, targetPtr)

    def raiseUnknownCommand (self, subCommand):
        raise Exception("Uknown command type: %s" % subCommand)

