#!/usr/bin/python

class TaskPointer:
    def __init__ (self, basePath):
        self.path = basePath
        self.name = self.extractTaskName(basePath)
        self.formPointerSubPaths(self.path)
        
    def __init__ (self, parentDir, name):
        self.path = appendSubDir(parentDir, name)
        self.name = name
        self.formPointerSubPaths(self.path)

    def extractTaskName (self, relPath):
        dirNames = relPath.split("/")
        nonEmptyNames = filter(lambda x: len(x) > 0, dirNames)
        return nonEmptyNames[-1]

    def formPointerSubPaths (self, relPath):
        self.descriptionPath = formTaskDescriptionPath(relPath)
        self.createDatePath = formTaskCreateDatePath(relPath)
        self.subTaskDirPath = formSubTaskDirPath(relPath)
        self.blockPath = formTaskBlockPath(relPath)

def createPointerOnDisk (taskPointer):
    createPointerDirOnDisk(taskPointer)
    createPointerPropertiesOnDisk(taskPointer)
    return taskPointer

def createPointerDirOnDisk (taskPointer):
    makeDirectory(taskPointer.basePath)

def createPointerPropertiesOnDisk (taskPointer):
    emptyProperites = TaskProperties()
    emptyProperties.writeToStore(taskPointer)

class TaskProperties:
    def __init__ (self, taskPointer, taskIDTracker):
        self.description = readString(taskPointer.descriptionPath, "")
        self.taskID = self.readTaskID(taskPointer.taskIDPath, taskIDTracker)
        self.createDate = self.readDate(taskPointer.createDatePath)
        self.blocks = self.readBlocks(taskPointer.blockPath)

    def __init__ (self):
        self.description = ""
        self.createDate = datetime.now()
        self.blocks = []

    def readTaskID (self, taskIDPath, taskIDTracker):
        readStr = readString(taskIDPath, "")
        return int(readStr) if readStr else \
            retrieveTaskID(taskIDPath, taskIDTracker)

    def retrieveTaskID (self, taskIDPath, taskIDTracker):
        taskID = taskIDTracker.incrementID()
        writeString(taskIDPath, str(taskID))
        return taskID

    def readDate (self, datePath):
        defaultDateStr = dateToString(datetime.now())
        dateStr = readString(taskPointer, defaultDateStr)
        return stringToDate(dateStr)

    def readBlocks (self, blockPath):
        blockStrs = readStrings(blockPath, [])
        return map(blockFromString, blockStrs)

    def writeToStore (self, taskPointer):
        self.writeString(self.description, taskPointer.descriptionPath)
        self.writeString(dateFromStr(self.createDate), taskPointer.createDatePath)
        self.writeStrings(map(blockFromStr, self.blocks), taskPointer.blockPath)
        self.writeSTring(str(self.taskID), taskPointer.taskIDPath)

def dateFromString (dateStr):
    dateFields = map(int, dateStr.split(","))
    d = date(dateFields[0], dateFields[1], dateFields[2])
    t = time(dateFields[3], dateFields[4], dateFields[5], dateFields[6])
    return datetime.combine(d, t)

def dateToString (dateTime):
    return "%d,%d,%d,%d,%d,%d,%d" % (year, month, day, hour, \
                                         minute, second, microsecond)

def diffDateToNow (dateOne):
    return diffDates(datetime.now() - dateOne)

def diffDates (dateOne, dateTwo):
    dateDelta = dateOne - dateTwo
    return (dateDelta.days, dateDelta.seconds)

def blockFromStr (blockStr):
    raise Exception('Block not implemented: %s' % blockStr)

def blockToStr (block):
    raise Exception('Block not implemented')

def pullSubTasks (taskPointer):
    subTaskDir = formSubDirPath(taskPointer.path)
    subDirs = pullDirectoriesInDirectory(subTaskDir)
    return map(lambda d: TaskPointer(d), subDirs)

class TaskAtom:
    def __init__ (self, taskPointer, taskProperites, subTasks):
    self.taskPointer = taskPointer
    self.taskProperties = taskProperties
    self.subTasks = subTasks

def assembleTaskPointer: (parentPointer, atomName):
    return TaskPointer(parentPointer, atomPath)

def createTaskPointer (parentPointer, atomName):
    return createPointerOnDisk(assembleTaskPointer(parentPointer, atomName))

def createTaskAtomDescribed (parentPointer, atomName, description):
    taskAtom = createTaskAtom(parentPointer, atomName)
    return addAndWriteTaskDescription(taskAtom, description)

def addAndWriteTaskDescription (taskAtom, description):
    taskAtom.taskProperties.description = description
    taskAtom.taskProperties.writeToStore()
    return taskAtom

def createTaskAtom (parentPointer, atomName):
    taskPointer = createTaskPointer(parentPointer, atomName)
    return assembleTaskAtom(taskPointer)

def assembleTaskAtom (parentPointer, atomName):
    taskPointer = assembleTaskPointer(parentPointer, atomName)
    return assembleTaskAtomFromPointer(taskPointer)

def assembleTaskAtom (taskPointer):
    taskProperties = TaskProperties(taskPointer)
    subTasks = pullSubTasks(taskPointer)
    return TaskAtom(taskPointer, taskProperties, subTasks)
    
