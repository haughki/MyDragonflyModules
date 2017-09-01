"""A command module for Dragonfly, for controlling notepad++.
-----------------------------------------------------------------------------
Licensed under the LGPL3.

"""

from dragonfly import Grammar, MappingRule, Dictation, Integer, Key, Text, IntegerRef, AppContext, Function
from supporting import utils


def printNumber(w, x=None, y=None, z=None):
    number = utils.buildNumber(w, x, y, z)
    Text(number).execute()

class CommandRule(MappingRule):
    mapping = {
        #"[go to | show] project window": Key("a-1"),

        # Search.
        "replace": Key("c-h"),
        "show find": Key("c-f"),
        "find <text>": Key("c-f/25") + Text("%(text)s"),
        # "find next": Key("f3"),
        # "find (prev | previous)": Key("s-f3"),
        "find in files": Key("cs-f"),

        # Code.
        "[shoreline | show] line <w> [<x>] [<y>] [<z>]": Key("c-g/25") + Function(printNumber)+ Key("enter"),
        "show white space": Key("cs-w"),
        
        # Window handling.
        "new tab": Key("c-n"),
        "next tab [<t>]": Key("c-tab:%(t)d"),
        "(preev | previous) tab [<t>]": Key("cs-tab:%(t)d"),
        "close tab": Key("c-w"),
        "(full-screen | full screen)": Key("f11"),
    }
    extras = [
        Integer("t", 1, 50),
        Dictation("text"),
        IntegerRef("n", 1, 50000),
        Integer("w", 0, 10),
        Integer("x", 0, 10),
        Integer("y", 0, 10),
        Integer("z", 0, 10)
    ]
    defaults = {
        "t": 1,
    }


context = AppContext(executable='notepad++')
grammar = Grammar('Notepad++ Grammar', context=context)

grammar.add_rule(CommandRule())
grammar.load()

# Unload function which will be called by natlink at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None