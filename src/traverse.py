#!/usr/bin/python

from taskAtom import *
from treeView import *

class TaskTree:
    def __init__ (self, taskPointer, depth):
        self.taskAtom = assembleTaskAtom(taskPointer)
        self.subTrees = []
        self.viewIdx = None
        self.depth = depth

    def sortSubTreesCreateDate (self):
        self.sortSubTreesFn(lambda x,y: ineqToCmp(x.createDate, y.createDate))

    def sortSubTreesFn (self, atomCmpFn):
        self.subTrees.sort(lambda x,y: atomCmpFn(x.taskAtom, y.taskAtom))
        map(lambda x: x.sortSubTreesFn(atomCmpFn), self.subTrees)

    def trackUserIdxView (self, userIdxView):
        self.viewIdx = userIdxView.addTaskPointer(self.taskAtom.taskPointer)
        map(lambda x: x.trackUserIdxView(userIdxView), self.subTrees)

def ineqToCmp (x, y):
    return 1 if x > y else -1

def traverseView (treeView):
    return traverseViewChild(treeView, "")

def traverseViewChild (treeView, childPath):
    topPointer = TaskPointer(treeView.relativeLocation.getFullChild(childPath))
    topTask = assembleTaskAtom(topPointer)
    return organizeTraverse(traverseTask(topTask, 0))

def organizeTraverse (taskTree, treeView):
    taskTree.sortSubTreesCreateDate()
    taskTree.trackUserIdxView(treeView.userIdxView)
    return taskTree

def traverseTask (taskPointer, dirDepth):
    taskTree = TaskTree(taskPointer, dirDepth)
    taskTree.subTrees = traverseSubTasks(taskTree, dirDepth+1)
    return taskTree

def traverseSubTasks (subTasks, dirDepth):
    return map(lambda p: traverseTask(p, dirDepth), subTasks)

