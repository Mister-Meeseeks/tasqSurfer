#!/usr/bin/python

def writeString (dataStr, filePath):
    writeStrings([dataStr], filePath)

def writeStrings (dataStrs, filePath):
    outStream = open(filePath, 'w')
    for dataStr in dataStrs:
        print >> outStream, dataStr

def readString (filePath):
    fileStrs = readStrings(filePath)
    return joinStoreStringsToSingle(fileStrs)

def joinStoreStringsToSingle (dataStrs):
    return "\n".join(dataStrs)

def readStrings (filePath):
    return open(filePath, 'r').readlines()

def readAttemptStrings (filePath, defaultVal):
    if (not os.exists(filePath)):
        writeStrings(filePath, defaultVal)
    return readStrings(filePath)

def readAttemptString (filePath, defaultVal):
    attemptVals = readAttemptStrings(filePath, [defaultVal])
    return joinStoreStringsToSingle(attemptVals)
