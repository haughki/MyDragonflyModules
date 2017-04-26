from dragonfly import Function
from dragonfly import Grammar, MappingRule, Integer, Key, Text, AppContext
from supporting import utils

def printNumber(w, x=None, y=None, z=None):
    number = utils.buildNumber(w, x, y, z)
    Text(number).execute()

class CommandRule(MappingRule):
    mapping = {
        # Window handling.
        "next tab [<t>]": Key("c-tab/40:%(t)d"),
        "(preev | previous) tab [<t>]": Key("cs-tab/40:%(t)d"),
        "close tab": Key("c-w"),
        
        # Edit
        "[shoreline | show] line <w> [<x>] [<y>] [<z>]": Key("f5/30") + Function(printNumber)+ Key("enter, escape"),
    }
    extras = [
        Integer("t", 1, 50),
        Integer("w", 0, 10),
        Integer("x", 0, 10),
        Integer("y", 0, 10),
        Integer("z", 0, 10),
    ]

    defaults = {
        "t": 1,
    }


winword_context = AppContext(executable="winword")
winword_grammar = Grammar("Microsoft Word", context=winword_context)
winword_grammar.add_rule(CommandRule())
winword_grammar.load()

# Unload function which will be called by natlink at unload time.
def unload():
    global winword_grammar
    if winword_grammar:
        print "unloading " + __name__ + "..."
        winword_grammar.unload()
    winword_grammar = None
