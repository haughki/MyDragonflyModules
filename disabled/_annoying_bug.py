from dragonfly import CompoundRule
from dragonfly import Grammar
from dragonfly import Key

class AnnoyingRule(CompoundRule):
    spec = "torch annoying bug"                  # Spoken form of command.

    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        Key("alt:up,s-down").execute()

annoying_grammar = Grammar("annoying bug")
annoying_grammar.add_rule(AnnoyingRule())
annoying_grammar.load()

def unload():
    global annoying_grammar
    if annoying_grammar:
        print "unloading " + __name__ + "..."
        annoying_grammar.unload()
    annoying_grammar = None