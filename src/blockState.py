#!/usr/bin/python

class BlockState:
    def __init__ (self, blockStrs):
        self.initEmpty()
        self.parseStrs(blockStrs)

    def initEmpty (self):
        self.skeleton = False
        self.active = False
        self.immediate = False
        self.essential = False

    def parseStrs (self, blockStrs):
        for blockStr in blockStrs:
            self.parseStr(blockStr.rstrip())        

    def parseStr (self, blockStr):
        if (blockStr == "skeleton"):
            self.skeleton = True
        elif (blockStr == "noSkeleton"):
            self.skeleton = False
        elif (blockStr == "active"):
            self.active = True
        elif (blockStr == "noActive"):
            self.active = False
        elif (blockStr == "immediate"):
            self.immediate = True
        elif (blockStr == "noImmediate"):
            self.immediate = False
        elif (blockStr == "essential"):
            self.essential = True
        elif (blockStr == "noEssential"):
            self.essential = False
        else:
            self.raiseBadBlockStr(blockStr)
        def raiseBadBlockStr (self, blockStr):
            raise Exception("Bad block string: %s" % blockStr)

    def convertToStrs (self):
        skeletonStrs = ["skeleton"] if self.skeleton else []
        activeStrs = ["active"] if self.active else []
        immediateStrs = ["immediate"] if self.immediate else []
        essentialStrs = ["essential"] if self.essential else []
        return skeletonStrs + activeStrs + immediateStrs + essentialStrs

def blocksFromStr (blockStrs):
    return BlockState(blockStrs)

def blocksToStr (blocks):
    return blocks.convertToStrs()
