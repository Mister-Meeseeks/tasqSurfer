#!/usr/bin/python

import sys
from commandExec import *
from repository import *
from revisionControl import *

changeDirToRepo()
execCommand(sys.argv)
revisionControlCommit(sys.argv)
