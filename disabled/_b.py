from dragonfly import *

def printBravo(): print "bravo"
def printEcho(): print "echo"
class BravoMap(MappingRule):
    mapping = {
        "print alpha": Function(printBravo),
        "print echo": Function(printEcho),
    }

bravo_rule = BravoMap()
bravo_grammar = Grammar("bravo")
bravo_grammar.add_rule(bravo_rule)
bravo_grammar.load()

def unload():
    global bravo_grammar
    if bravo_grammar:
        print "unloading " + __name__ + "..."
        bravo_grammar.unload()
    bravo_grammar = None