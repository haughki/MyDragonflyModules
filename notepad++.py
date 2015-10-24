"""A command module for Dragonfly, for controlling notepad++.
-----------------------------------------------------------------------------
Licensed under the LGPL3.

"""

from dragonfly import Grammar, MappingRule, Dictation, Integer, Key, Text, IntegerRef, AppContext

class CommandRule(MappingRule):
    mapping = {
        #"[go to | show] project window": Key("a-1"),

        # Search.
        "find (text | it)": Key("c-f"),
        "find in files": Key("cs-f"),

        # Code.
        "[go to | show] line <n>": Key("c-g/25") + Text("%(n)d") + Key("enter"),
        #"(full-screen | full screen)": Key("cs-x"),

        # Window handling.
        "next tab [<t>]": Key("c-tab:%(t)d"),
        "(preev | previous) tab [<t>]": Key("cs-tab:%(t)d"),
        "close tab": Key("c-w"),
    }
    extras = [
        Integer("t", 1, 50),
        Dictation("text"),
        IntegerRef("n", 1, 50000)
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