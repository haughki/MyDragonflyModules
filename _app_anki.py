"""A command module for Dragonfly, for controlling VSCode.
-----------------------------------------------------------------------------
Licensed under the LGPL3.

"""

from dragonfly import Grammar, MappingRule, Dictation, Integer, Key, Text, IntegerRef, AppContext, Pause, Mouse
from supporting import utils

class AnkiMapping(MappingRule):

    mapping = {
        "add card": Key("c-enter"),
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


context = AppContext(executable='anki')
anki_grammar = Grammar('Anki Grammar', context=context)
anki_grammar.add_rule(AnkiMapping())
anki_grammar.load()

def unload():
    global anki_grammar
    anki_grammar = utils.unloadHelper(anki_grammar, __name__)
