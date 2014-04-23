#!/usr/bin/python

from dirLayout import *

class DirectoryOwner:
    def __init__ (self, path):
        self.path = path
        createDirectoryIfNeeded(self.path)

class FileStore:
    def __init__ (self, filePath, dfltValue, convertFromReadFn, convertToWriteFn):
        self.filePath = filePath
        self.convertToWriteFn = convertToWriteFn
        self.convertFromReadFn = convertFromReadFn
        self.value = self.loadInitValue(dfltValue)

    def saveToStore (self):
        self.saveValue(self.value)

    def saveValue (self, value):
        writeStrings(self.convertToWriteFn(value), self.filePath)

    def loadInitValue (self, dfltVal):
        if (not fileExists(self.filePath)):
            self.saveValue(dfltVal)
        return self.loadValue()

    def loadValue (self):
        return self.convertFromReadFn(readStrings(self.filePath))

class FileStoreList (FileStore):
    def __init__ (self, filePath, dfltVal=[], \
                      fromStrFn = lambda x: x, toStrFn = str):
        FileStore.__init__(self, filePath, dfltVal, \
                               lambda x: map(fromStrFn,x), \
                               lambda x: map(toStrFn,x))

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

    def dictToStrs (self, dictStrs, keyToStr, valToStr):
        return map(lambda x: "%s\t%s" % (keyToStr(x), valToStr(x)), dictStrs)
        
def writeStrings (dataStrs, filePath):
    outStream = open(filePath, 'w')
    for dataStr in dataStrs:
        print >> outStream, dataStr

def readStrings (filePath):
    return open(filePath, 'r').readlines()

def joinStringLines (dataStrs):
    return "\n".join(dataStrs)
