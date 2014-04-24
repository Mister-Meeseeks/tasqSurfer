#!/usr/bin/python

from taskAtom import *
from treeView import *

class TaskTree:
    def __init__ (self, taskPointer, depth):
        self.taskAtom = TaskAtomReadOnly(taskPointer)
        self.subTrees = []
        self.viewIdx = None
        self.depth = depth

    def sortSubTreesCreateDate (self):
        self.sortSubTreesFn(lambda x,y: ineqToCmp\
                                (x.taskProperties.createDate.value, \
                                     y.taskProperties.createDate.value))

    def sortSubTreesFn (self, atomCmpFn):
        self.subTrees.sort(lambda x,y: atomCmpFn(x.taskAtom, y.taskAtom))
        map(lambda x: x.sortSubTreesFn(atomCmpFn), self.subTrees)

    def trackUserIdxView (self, userIdxView):
        self.viewIdx = userIdxView.addTaskPointer(self.taskAtom.taskPointer)
        map(lambda x: x.trackUserIdxView(userIdxView), self.subTrees)

def ineqToCmp (x, y):
    return 1 if x > y else -1

def traverseView (treeView):
    return traverseViewPath(treeView, treeView.relativeLocation.getFullPath())

def traverseViewPath (treeView, taskPath):
    treeView.userIdxView.resetIdxToPointer()
    topPointer = TaskPointer(taskPath)
    return organizeTraverse(traverseTask(topPointer, 0), treeView)

def organizeTraverse (taskTree, treeView):
    taskTree.sortSubTreesCreateDate()
    taskTree.trackUserIdxView(treeView.userIdxView)
    return taskTree

def traverseTask (taskPointer, dirDepth):
    taskTree = TaskTree(taskPointer, dirDepth)
    taskTree.subTrees = traverseSubTasks(taskTree.taskAtom.subTasks, dirDepth+1)
    return taskTree

def traverseSubTasks (subTasks, dirDepth):
    return map(lambda p: traverseTask(p, dirDepth), subTasks)

