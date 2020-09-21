from dragonfly import MappingRule, Function

def printKilo(): print "kilo"
def printLima(): print "lima"
class KiloMap(MappingRule):
    mapping = {
        "print kilo": Function(printKilo),
        "print lima": Function(printLima),
    }

