#!/usr/bin/python

from taskAtom import *

def displayTree (treeView, traverseTree):
    printTargetLocation(treeView, traverseTree)
    displayTreeTraverse(traverseTree)

def displayTreeTraverse (traverseTree):
    displayParams = DisplayParams()
    displayLines = convertToDisplayLines(traverseTree, displayParams)
    DisplayFieldPrinter(displayLines)

def convertToDisplayLines (traverseTree, displayParams):
    x = DisplayHeaderFields()
    return [DisplayHeaderFields()] + \
        convertToBodyDisplay(traverseTree, displayParams)

def convertToBodyDisplay (traverseTree, displayParams):
    if (traverseTree.depth <= displayParams.maxDepth):
        return convertToBodyDisplayLines(traverseTree, displayParams)
    else:
        return []

def convertToBodyDisplayLines (traverseTree, displayParams):
    topFields = DisplayLineFields(traverseTree, displayParams)
    subFields = map(lambda t: convertToBodyDisplay(t, displayParams), \
                        traverseTree.subTrees)
    return [topFields] + reduce(lambda x,y: x + y, subFields, [])

class DisplayParams:
    def __init__ (self):
        self.maxDepth = 4
        self.descendSpaces = 2
        self.maxDescrChars = 100

class DisplayFieldPrinter:
    def __init__ (self, displayLines):
        self.deriveFieldLens(displayLines)
        self.printFieldLines(displayLines)

    def deriveFieldLens (self, displayLines):
        self.viewIdxLen = self.getFieldSize(displayLines, lambda x: x.viewIdx)
        self.nameLen = self.getFieldSize(displayLines, lambda x: x.name)
        self.ageLen = self.getFieldSize(displayLines, lambda x: x.age)
        self.descrLen = self.getFieldSize(displayLines, lambda x: x.descr)

    def getFieldSize (self, displayLines, getFn):
        return max(map(len, map(getFn, displayLines)))

    def printFieldLines (self, displayLines):
        self.printHeaderLine(displayLines[0])
        self.printBodyLines(displayLines[1:])

    def printHeaderLine (self, headerFieldLine):
        self.printFieldLine(headerFieldLine)
        self.printHeaderSep()

    def printBodyLines (self, bodyLines):
        #self.printRootBodyLine(bodyLines)
        self.printNodeBodyLines(bodyLines)

    def printRootBodyLine (self, bodyLines):
        if (len(bodyLines) > 0):
            self.printFieldLine(bodyLines[0])
            self.printHeaderSep()

    def printNodeBodyLines (self, bodyLines):
        for bodyLine in bodyLines[1:]:
            self.printFieldLine(bodyLine)        

    def printHeaderSep (self):
        print "%s  %s  %s  %s" % \
            (repeatCharForLen("-", self.viewIdxLen),
             repeatCharForLen("-", self.nameLen),
             repeatCharForLen("-", self.ageLen),
             repeatCharForLen("-", self.descrLen))

    def printFieldLine (self, fieldLine):
        print "%s  %s  %s  %s" % \
            (self.formatField(fieldLine.viewIdx, self.viewIdxLen),
             self.formatField(fieldLine.name, self.nameLen),
             self.formatField(fieldLine.age, self.ageLen),
             self.formatField(fieldLine.descr, self.descrLen))

    def formatField (self, fieldStr, fieldLen):
        numFillerSpaces = fieldLen - len(fieldStr)
        return fieldStr + repeatSpaceForLen(fieldLen - len(fieldStr))

class DisplayHeaderFields:
    def __init__ (self):
        self.viewIdx = "Idx"
        self.name = "Name"
        self.age = "Age"
        self.descr = "Description"

class DisplayLineFields:
    def __init__ (self, taskTree, displayParams):
        self.viewIdx = self.formViewIdxStr(taskTree, displayParams)
        self.name = self.formNameStr(taskTree, displayParams)
        self.age = self.formAgeStr(taskTree, displayParams)
        self.descr = self.formDescrStr(taskTree, displayParams)

    def formViewIdxStr (self, taskTree, displayParams):
        return str(taskTree.viewIdx)

    def formNameStr (self, taskTree, displayParams):
        indentDepth = max((taskTree.depth - 1), 0)
        return repeatSpaceForLen(indentDepth * displayParams.descendSpaces) \
            + taskTree.taskAtom.taskPointer.name

    def formDescrStr (self, taskTree, displayParams):
        descr = taskTree.taskAtom.taskProperties.description.value
        return descr[:displayParams.maxDescrChars]

    def formAgeStr (self, taskTree, displayParams):
        createDate = taskTree.taskAtom.taskProperties.createDate.value
        (days, seconds) = diffDateToNow(createDate)
        if (days > 14):
            return "%dw" % (days / 7)
        if (days > 0):
            return "%dd" % days
        elif (seconds > 7200):
            return "%dh" % (seconds / 3600)
        elif (seconds > 120):
            return "%dm" % (seconds / 60)
        else:
            return "%ds" % seconds

def repeatSpaceForLen (numSpaces):
    return repeatCharForLen(" ", numSpaces)

def repeatCharForLen (charVal, numChars):
    return reduce(lambda x,y: x + charVal, range(numChars), "")
    
def printRelativeLocation (treeView):
    loc = treeView.relativeLocation.getTreeLocation()
    print "Tree location: %s" % loc

def printTargetLocation (treeView, traverseTree):
    taskPath = traverseTree.taskAtom.taskPointer.path
    loc = treeView.relativeLocation.getTreeLocationRepo(taskPath)
    print "Tree location: %s" % loc
