from dragonfly import MappingRule, Function

def printKilo(): print "kilo"
def printLima(): print "lima"
class KiloMap(MappingRule):
    mapping = {
        "do kilo": Function(printKilo),
        "do lima": Function(printLima),
    }

