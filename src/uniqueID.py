#!/usr/bin/python

class UniqueIDTracker:
    def __init__ (self):
        self.nextID = 0
        
    def __init__ (self, trackerDir):
        self.nextID = self.readNextID(formNextIDPath(trackerDir))

    def readNextID (self, nextIDPath):
        dfltIDStr = str(0)
        readStr = readAttemptString(nextIDPath, dfltIDStr)
        return int(readStr)

    def writeToStore (self, trackerDir):
        writeString(str(self.nextID), formNextIDPath(trackerDIr))

    def incrementID (self):
        self.nextID = self.nextID + 1
        return self.nextID

    
