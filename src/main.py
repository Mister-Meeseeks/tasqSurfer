#!/usr/bin/python

import sys
from commandExec import *
from repository import *
from revisionControl import *

changeDirToRepo()
CommandExec().execCommand(sys.argv)
