#!/usr/bin/python

def execCommand (args):
    subCommand = extractSubCommand(args)
    subArgs = estractSubCommandArgs(args)
    execCommandArgs(subCommand, subArgs)

def execCommandArgs (subCommand, subArgs):
    if (subCommand in addCommandKeywords):
        execAddCommand(AddCommand(subArgs))
    elif (subCommand in listCommandKeywords):
        execListCommand(ListCommand(subArgs))
    elif (subCommand in cdCommandKeywords):
        execCdCommand(CdCommand(subArgs))
    elif (subCommand in moveCommandKeywords):
        execMoveCommand(MoveCommand(subArgs))
    elif (subCommand in doneCommandKeywords):
        execDoneCommand(DoneCommand(subArgs))
    elif (subCommand in rmCommandKeywords):
        execRmCommand(RmCommand(subArgs))
    elif (subCommand in stageCommandKeywords):
        execStageCommand(StageCommand(subArgs))
    elif (subCommand in unstageCommandKeywords):
        execUnstageCommand(UnstageCommand(subArgs))
    else:
        raiseUnknownCommand(subCommand)

def execAddCommand (addCmd):
    treeView = TreeView(retrieveTreeViewPath())
    parentPointer = convertTargetStrToPointer(addCmd.parentTareget, treeView)
    taskAtom = createTaskAtomDescribed(parentPointer, addCmd.name, addCmd.descr)
    revisionControlAdd(taskAtom.taskPointer.path)

def execListCommand (listCmd):
    treeView = TreeView(retrieveTreeViewPath())
    listPointer = convertTargetStrToPointer(listCmd.target, treeView)
    taskTree = traverseView(treeView, listPointer)
    displayTree(taskTree)
    treeView.writeToStore()

def execCdCommand (cdCmd):
    treeView = TreeView(retrieveTreeViewPath())
    cdPointer = convertTargetStrToPointer(cdCmd.target, treeView)
    treeView.relativePath.changePath(cdPointer)
    treeView.writeToStore()

def execMoveCommand (moveCmd):
    treeView = TreeView(retrieveTreeViewPath())
    sourcePtr = convertTargetStrToPointer(moveCmd.source, treeView)
    targetPtr = convertTargetStrToPointer(moveCmd.target, treeView)
    revisionControlMove(sourcePtr.path, targetPtr.path)

def execDoneCommand (doneCmd):
    treeView = TreeView(retrieveTreeViewPath())
    sourcePtr = convertTargetStrToPointer(doneCmd.source, treeView)
    revisionControlRm(sourcePtr.path)

def execRmCommand (rmCmd):
    treeView = TreeView(retrieveTreeViewPath())
    sourcePtr = convertTargetStrToPointer(rmCmd.source, treeView)
    revisionControlRm(sourcePtr.path)

def execStageCommand (stageCmd):
    if (stageCmd.name == ""):
        execStageListCommand(stageCmd)
    else:
        execStageAddCommand(stageCmd)

def execStageListCommand (stageCmd):
    stageView = TreeView(retrieveStageViewPath())
    taskTree = traverseView(stageView)
    displayTree(taskTree)
    stageView.writeToStore()

def execStageAddCommand (stageCmd):
    stageView = TreeView(retrieveStageViewPath())
    parentPointer = convertTargetStrToPointer("", stageView)
    taskAtom = createTaskAtomDescribed(parentPointer, addCmd.name, addCmd.descr)
    revisionControlAdd(taskAtom.taskPointer.path)

def execUnstageCommand (unstageCmd):
    if (unstageCmd.treeParentPointer == ""):
        execUnstageRmCommand(unstageCmd)
    else:
        execUnstageAddCommand(unstageCmd)

def execUnstageRmCommand (unstageCmd):
    stageView = TreeView(retrieveStageViewPath())
    sourcePtr = convertTargetStrToPointer(unstageCmd.source, stageView)
    revisionControlRm(sourcePtr.path)    

def execUnstageAddCommand (unstageCmd):
    stageView = TreeView(retrieveStageViewPath())
    treeView = TreeView(retrieveTreeViewPath())
    sourcePtr = convertTargetStrToPointer(unstageCmd.source, stageView)
    targetPtr = convertTargetStrToPointer(unstageCmd.source, treeView)
    revisionControlMv(sourcePtr.path, targetPtr.path)

def raiseUnknownCommand (subCommand):
    raise Exception("Uknown command type: %s" % subCommand)
