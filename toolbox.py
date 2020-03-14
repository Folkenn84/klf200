##
## AHM, 2018 
##

def getIndex(sourceDict, value):
    return (k for k, v in sourceDict.items() if v == value).__next__()

def toHex(s):
    return ":".join("{:02x}".format(c) for c in s)
