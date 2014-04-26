#!/usr/bin/python

from dirLayout import *

class DirectoryOwner:
    def __init__ (self, path):
        self.path = path
        createDirectoryIfNeeded(self.path)

class FileLoader:
    def __init__ (self, filePath, convertFromReadFn):
        self.filePath = filePath
        self.convertFromReadFn = convertFromReadFn
    def loadValue (self):
        return self.convertFromReadFn(readStrings(self.filePath))

class FileSaver:
    def __init__ (self, filePath, convertToWriteFn):
        self.filePath = filePath
        self.convertToWriteFn = convertToWriteFn
    def saveToStore (self):
        self.saveValue(self.value)
    def saveValue (self, value):
        writeStrings(self.convertToWriteFn(value), self.filePath)

class FileReader (FileLoader):
    def __init__ (self, filePath, convertFromReadFn):
        FileLoader.__init__(self, filePath, convertFromReadFn)
        self.value = self.loadValue()

class FileStore (FileLoader, FileSaver):
    def __init__ (self, filePath, dfltValue, convertFromReadFn, convertToWriteFn):
        FileLoader.__init__(self, filePath, convertFromReadFn)
        FileSaver.__init__(self, filePath, convertToWriteFn)
        self.value = self.loadInitValue(dfltValue)

    def loadInitValue (self, dfltVal):
        if (not fileExists(self.filePath)):
            self.saveValue(dfltVal)
        return self.loadValue()

class FileReaderList (FileReader):
    def __init__ (self, filePath, fromStrFn = lambda x: x):
        FileReader.__init__(self, filePath, \
                                lambda x: map(fromStrFn, x))

class FileStoreList (FileStore):
    def __init__ (self, filePath, dfltVal=[], \
                      fromStrFn = lambda x: x, toStrFn = str):
        FileStore.__init__(self, filePath, dfltVal, \
                               lambda x: map(fromStrFn, x), \
                               lambda x: map(toStrFn, x))

class FileReaderSingle (FileReader):
    def __init__ (self, filePath, fromStrFn = lambda x: x):
        FileReader.__init__(self, filePath, \
                                lambda x: fromStrFn(joinStringLines(x)))

class FileStoreSingle (FileStore):
    def __init__ (self, filePath, dfltVal="", \
                      fromStrFn = lambda x: x, toStrFn = str):
        FileStore.__init__(self, filePath, dfltVal, \
                               lambda x: fromStrFn(joinStringLines(x)), \
                               lambda x: [toStrFn(x)])

class FileStoreDict (FileStore):
    def __init__ (self, filePath, dfltVal={}, \
                      keyFromStr = lambda x: x, valFromStr = lambda x: x, \
                      keyToStr = str, valToStr = str):
        FileStore.__init__(self, filePath, dfltVal,
                           lambda x: self.dictFromStrs(x,keyFromStr,valFromStr),
                           lambda x: self.dictToStrs(x,keyToStr,valToStr))

    def dictFromStrs (self, dictStrs, keyFromStr, valFromStr):
        retDict = {}
        for dictStr in dictStrs:
            dictFields = dictStr.split("\t")
            retDict[keyFromStr(dictFields[0])] = valFromStr(dictFields[1])
        return retDict

    def dictToStrs (self, dictVal, keyToStr, valToStr):
        return map(lambda x: "%s\t%s" % \
                       (keyToStr(x), valToStr(dictVal[x])), dictVal)
        
def writeStrings (dataStrs, filePath):
    outStream = open(filePath, 'w')
    for dataStr in dataStrs:
        print >> outStream, dataStr

def readStrings (filePath):
    fileStrs = open(filePath, 'r').readlines()
    return map(stripInputString, fileStrs)

def stripInputString (dataStr):
    return dataStr.rstrip()

def joinStringLines (dataStrs):
    return "\n".join(map(lambda x: x, dataStrs))
