"""A command module for Dragonfly, for controlling VSCode.
-----------------------------------------------------------------------------
Licensed under the LGPL3.

"""

from dragonfly import Grammar, MappingRule, Dictation, Integer, Key, Text, IntegerRef, AppContext, Pause, Mouse
from supporting import utils

class WslMapping(MappingRule):

    mapping = {
        "project[s]": Text("proj") + Key("enter"),
        "Windows temp": Text("dtemp") + Key("enter"),
        "hawk user": Text("hawk") + Key("enter"),
    }

    extras = [
        Integer("t", 1, 50),
        Dictation("text"),
        Dictation("text2"),
        IntegerRef("n", 1, 50000),
        Integer("w", 0, 10),
        Integer("x", 0, 10),
        Integer("y", 0, 10),
        Integer("z", 0, 10)
    ]
    defaults = {
        "t": 1,
        "text": "",
        "text2": ""
    }


context = AppContext(executable='ubuntu')
wsl_grammar = Grammar('Ubuntu', context=context)
wsl_grammar.add_rule(WslMapping())
wsl_grammar.load()

def unload():
    global wsl_grammar
    wsl_grammar = utils.unloadHelper(wsl_grammar, __name__)
