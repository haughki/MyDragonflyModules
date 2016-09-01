from dragonfly import *

def printAlpha(): print "alpha"
def printDelta(): print "delta"
class AlphaMap(MappingRule):
    mapping = {
        "print alpha": Function(printAlpha),
        "print delta": Function(printDelta),
    }

alpha_rule = AlphaMap()
alpha_grammar = Grammar("alpha")
alpha_grammar.add_rule(alpha_rule)
alpha_grammar.load()

def unload():
    global alpha_grammar
    if alpha_grammar:
        print "unloading " + __name__ + "..."
        alpha_grammar.unload()
    alpha_grammar = None