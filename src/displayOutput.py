#!/usr/bin/python

def displayTree (traverseTree):
    displayParams = DisplayParams()
    displayLines = converToDisplayLines(traverseTree, displayParams)
    DisplayFieldOutputter(displayLines)

def convertToDisplayLines (traverseTree, displayParams):
    return [DisplayHeaderFields()] + \
        convertToBodyDisplayLines(traverseTree, displayParams)

def convertToBodyDisplayLines (traverseTree, dislplayParams):
    topFields = DisplayLineFields(traverseTree, displayParams)
    subFields = map(lambda t: convertToBodyDisplayLines(t, displayParams), \
                        traverseTree.subTrees)
    return [topFields] + reduce(lambda x,y: x + y, subFields)

class DisplayParams:
    def __init__ (self):
        self.maxDepth = 4
        self.descendSpaces = 2
        self.maxDescrChars = 100

class DisplayFieldOutputer:
    def __init__ (self, fieldLines):
        self.deriveFieldLens(fieldLines):
        self.printFieldLines(fieldLines)

    def deriveFieldLens (self, fieldLines)
        self.viewIdxLen = self.getFieldSize(displayLines, lambda x: x.viewIdx)
        self.nameLen = self.getFieldSize(displayLines, lambda x: x.name)
        self.ageLen = self.getFieldSize(displayLines, lambda x: x.age)
        self.descrLen = self.getFieldSize(displayLines, lambda x: x.descr)

    def getFieldSize (self, displayLines, getFn):
        return max(map(getFn, displayLines))

    def printFieldLines (self, fieldLines):
        self.printHeaderLine(fieldLines[0])
        self.printBodyLines(fieldLines[1:])

    def printHeaderLine (self, headerFieldLine):
        self.printFieldLine(headerFieldLine)
        self.printHeaderSep()

    def printFieldLine (self, fieldLine):
        print "%s %s %s %s" % \
            (self.formatField(fieldLine.viewIdx, self.viewIdxLen),
             self.formatField(fieldLine.name, self.nameIdxLen),
             self.formatField(fieldLine.age, self.ageLen),
             self.formatField(fieldLine.descr, self.descrLen))

    def formatField (self, fieldStr, fieldLen):
        return fieldStr + repeatSpaceForLen(fieldLen)

class DisplayHeaderFields:
    def __init_ (self):
        self.viewIdx = "Idx"
        self.name = "Name"
        self.age = "Age"
        self.descr = "Description"

class DisplayLineFields:
    def __init__ (self, taskTree, displayParams):
        self.viewIdx = self.formViewIdxStr(taskTree, displayParams)
        self.name = self.formNameStr(taskTree, displayParams)
        self.age = self.formAgeStr(taskTree, displayParams)
        self.descr = self.formDescr(taskTree, displayParams)

    def formViewIdxStr (self, taskTree, displayParams):
        return int(taskTree.viewIdx)

    def formNameStr (self, taskTree, displayParams):
        return repeatSpaceForLen(taskTree.depth * displayParams.descendSpaces)
            + taskTree.taskAtom.taskPointer.name

    def formDescrStr (self, taskTree, displayParams):
        descr = taskTree.taskAtom.taskProperties.description
        return descr[:displayParams.maxDescrChars]

    def formAgeStr (self, taskTree, displayParams):
        createDate = taskTree.taskAtom.taskProperties.createDate
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
    return reduce(lambda x,y: x + " ", range(numSpaces), " ")

