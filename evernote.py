"""A command module for Dragonfly, for controlling Evernote
-----------------------------------------------------------------------------
Licensed under the LGPL3.

"""

from dragonfly import Grammar, MappingRule, Dictation, Integer, Key, Text, IntegerRef, AppContext
from supporting import utils


class CommandRule(MappingRule):
    mapping = {
        # Search.
        "replace": Key("c-h"),
        "show find": Key("c-f"),
        "find <text>": Key("c-f/25") + Text("%(text)s"),
        "find next": Key("c-g"),
        "find (prev | previous)": Key("cs-g"),
        "note find": Key("c-q"),
        "note find <text>": Key("c-q/25") + Text("%(text)s"), 
        
        # Window handling.
        # "new tab": Key("c-n"),
        # "next tab [<t>]": Key("c-tab:%(t)d"),
        # "(preev | previous) tab [<t>]": Key("cs-tab:%(t)d"),
        # "close tab": Key("c-w"),
        # "(full-screen | full screen)": Key("f11"),
    }
    extras = [
        Integer("t", 1, 50),
        Dictation("text"),
        IntegerRef("n", 1, 50000),
    ]
    defaults = {
        "t": 1,
    }


context = AppContext(executable='evernote')
evernote_grammar = Grammar('Evernote Grammar', context=context)

evernote_grammar.add_rule(CommandRule())
evernote_grammar.load()

# Unload function which will be called by natlink at unload time.
def unload():
    global evernote_grammar
    evernote_grammar = utils.unloadHelper(evernote_grammar, __name__)
