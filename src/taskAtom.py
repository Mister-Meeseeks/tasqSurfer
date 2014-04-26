#!/usr/bin/python

import datetime
from storeFile import *
from dirLayout import *
from blockState import *

class TaskPointer (DirectoryOwner):
    def __init__ (self, pointerPath):
        DirectoryOwner.__init__ (self, pointerPath)
        self.name = self.extractTaskName()
        self.formPointerSubPaths()

    def extractTaskName (self):
        dirNames = self.path.split("/")
        nonEmptyNames = filter(lambda x: len(x) > 0, dirNames)
        return nonEmptyNames[-1]

    def formPointerSubPaths (self):
        self.taskIDPath = formTaskIDPath(self.path)
        self.descriptionPath = formTaskDescriptionPath(self.path)
        self.createDatePath = formTaskCreateDatePath(self.path)
        self.blockPath = formTaskBlockPath(self.path)

    def __str__ (self):
        return self.path

class TaskPropertiesReadOnly:
    def __init__ (self, taskPointer):
        self.description = FileReaderSingle(taskPointer.descriptionPath)
        self.createDate = FileReaderSingle(taskPointer.createDatePath, dateFromStr)
        self.blocks = FileReader(taskPointer.blockPath, BlockState)
        self.taskID = FileReaderSingle(taskPointer.taskIDPath, int)

class TaskProperties:
    def __init__ (self, taskPointer, taskIDTracker):
        self.description = FileStoreSingle(taskPointer.descriptionPath, "")
        self.createDate = FileStoreSingle(taskPointer.createDatePath, 
                                          nowDate(), dateFromStr, dateToStr)
        self.blocks = FileStore(taskPointer.blockPath, BlockState([]),
                                blocksFromStr, blocksToStr)
        self.taskID = FileStoreSingle(taskPointer.taskIDPath, 
                                      taskIDTracker.getNextID(), int)
        self.incrementTaskIDIfUsed(taskIDTracker)

    def incrementTaskIDIfUsed (self, taskIDTracker):
        if (self.taskID == taskIDTracker.getNextID()):
            taskIDTracker.incrementID()

    def saveToStore (self):
        self.taskID.saveToStore()
        self.description.saveToStore()
        self.createDate.saveToStore()
        self.blocks.saveToStore()

def nowDate():
    return datetime.datetime.now()

def dateFromStr (dateStr):
    fields = map(int, dateStr.split(","))
    d = datetime.date(fields[0], fields[1], fields[2])
    t = datetime.time(fields[3], fields[4], fields[5], fields[6])
    return datetime.datetime.combine(d, t)

def dateToStr (d):
    return "%d,%d,%d,%d,%d,%d,%d" % (d.year, d.month, d.day, d.hour, \
                                         d.minute, d.second, d.microsecond)

def diffDateToNow (dateOne):
    return diffDates(nowDate(), dateOne)

def diffDates (dateOne, dateTwo):
    dateDelta = dateOne - dateTwo
    return (dateDelta.days, dateDelta.seconds)

def blockFromStr (blockStr):
    raise Exception('Block not implemented: %s' % blockStr)

def blockToStr (block):
    raise Exception('Block not implemented')

def pullSubTasks (taskPointer):
    subDirs = pullDirectories(taskPointer.path)
    return map(lambda d: TaskPointer(d), subDirs)

class TaskAtom:
    def __init__ (self, taskPointer, taskIDTracker):
        self.taskPointer = taskPointer
        self.taskProperties = TaskProperties(taskPointer, taskIDTracker)
        self.subTasks = pullSubTasks(taskPointer)

class TaskAtomReadOnly:
    def __init__ (self, taskPointer):
        self.taskPointer = taskPointer
        self.taskProperties = TaskPropertiesReadOnly(taskPointer)
        self.subTasks = pullSubTasks(taskPointer)
        
def createTaskPointerOnParent (parentPointerPath, atomName):
    pointerPath = formSubDirectory(parentPointerPath, atomName)
    return TaskPointer(pointerPath)

def getTaskBlocks (taskAtom):
    return taskAtom.taskProperties.blocks.value
