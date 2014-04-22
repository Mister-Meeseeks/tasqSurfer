#!/usr/bin/python

class TaskTree:
    def __init__ (self, taskPointer):
        self.taskAtom = assembleTaskAtom(taskPointer)
        self.subTrees = []
        self.depth = None

    def appendTree (self, taskTree):
        taskTree.incrementDepth()
        self.subTrees.append(taskTree)

    def appendTrees (self, taskTrees):
        for taskTree in taskTrees:
            self.appendTree(taskTree)

def traverseView (treeView):
    topTask = assembleTaskAtom(treeView.relativePath.getFullPath())
    return traverseTask(topTask)

def traverseTask (taskPointer):
    TaskTree taskTree (taskPointer)
    subTrees = traverseDepthTasks(taskTree)
    taskTree.appendTrees(subTrees)
    return taskTree

def traverseDepthTasks (subTasks, params, dirDepth):
    return traverseSubTasks(subTasks, params, dirDepth) \
        if hasMoreDepth(params, dirDepth) else []        

def traverseSubTasks (subTasks, params, dirDepth):
    return map(traverseView, subTasks)

def markTreePositions (taskTree, treeView):
    markTreePositions(taskTree, treeView, 1)

def markTreePositions (taskTree, treeView, depth):
    markTreePointer(taskTree, treeView)
    taskTree.markDepth(depth)
    markSubTrees(taskTree, treeView, depth)

def markTreePointer (taskTree, treeView):
    taskPointer = taskTree.taskAtom.taskPointer
    treeView.userIdxView.addTaskPointer(taskPointer)
    
def markSubTrees (taskTree, treeView, depth):
    map(lambda t: markTreePositions(t, treeView, depth+1), \
            taskTree.subTrees)

