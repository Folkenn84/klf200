##
## AHM, 2018 
##

from slip import *

LoopDelay = 1


def getIndex(sourceDict, value):
    return (k for k, v in sourceDict.items() if v == value).__next__()


def toHex(s):
    return ":".join("{:02x}".format(c) for c in s)


def parse_command(command, start=2, end=4):
    return int(toHex(slip_unpack(command)[start:end]).replace(':', ''), 16)
