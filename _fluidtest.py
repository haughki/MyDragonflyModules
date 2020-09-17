

### SO FAR, I CANNOT GET THIS TO WORK

from dragonfly import (Integer, Key, Text, Dictation)

from dragonfluid import ActiveGrammarRule, GlobalRegistry, FluidRule, QuickFluidRules
from supporting import utils


grammar = GlobalRegistry("fluid one")

@ActiveGrammarRule(grammar)
class fluidOne(QuickFluidRules):
    name="fluid_one"
    mapping = {
        "snarl": Key("space, s, n, a, r, space"),
        "burp": Text(" burpy "),
        "groan": Text("  g r o aaa n  "),
    }
    extras=[
        Integer("n", 1, 50),
        Integer("tab", 1, 8),
        Integer("number", 1, 9999),
        Dictation("text"),
    ]
    defaults = {
        "n": 1,
    }


#grammar.add_rule(fluidOne(grammar))
grammar.load()

def unload():
    global grammar
    grammar = utils.unloadHelper(grammar, __name__)