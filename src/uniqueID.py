#!/usr/bin/python

from storeFile import *
from dirLayout import *

class UniqueIDTracker (DirectoryOwner):
    def __init__ (self, trackerDirPath):
        DirectoryOwner.__init__(self, trackerDirPath)
        self.nextID = FileStoreSingle(formNextIDPath(self.path), 0, int)

    def saveToStore (self):
        self.nextID.saveToStore()

    def incrementID (self):
        self.nextID = self.nextID + 1
        
    def getNextID (self):
        return self.nextID.value


    
