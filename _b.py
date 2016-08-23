from dragonfly import *

def printBravo(): print "bravo"
def printEcho(): print "echo"
class BravoMap(MappingRule):
    mapping = {
        "print bravo": Function(printBravo),
        "print echo": Function(printEcho),
    }

