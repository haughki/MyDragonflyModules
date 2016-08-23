from dragonfly import *


def printAlpha(): print "alpha"
def printDelta(): print "delta"
class AlphaMap(MappingRule):
    mapping = {
        "print alpha": Function(printAlpha),
    }



