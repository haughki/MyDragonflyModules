from dragonfly import *

def printTango(): print "tango"
def printUniform(): print "uniform"
class TangoMap(MappingRule):
    mapping = {
        "print tango": Function(printTango),
        "print uniform": Function(printUniform),
    }
