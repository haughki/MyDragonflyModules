
"""A command module for Dragonfly, for controlling VSCode.
-----------------------------------------------------------------------------
Licensed under the LGPL3.

"""

from dragonfly import Grammar, MappingRule, Dictation, Integer, Key, Text, IntegerRef, AppContext, Pause, Mouse
from supporting import utils



# def T(s, pause=0.00001, **kws):
#     return Text(s, pause=pause, **kws)

def T(s, **kws):
    return Text(s, **kws)

def K(*args, **kws):
    return Key(*args, **kws)

def P(*args, **kws):
    return Pause(*args, **kws)

def M(*args, **kws):
    return Mouse(*args, **kws)

class MobaXtermMapping(MappingRule):

    mapping = {
        "next tab [<t>]": Key("c-tab:%(t)d"),
        "(preev | previous) tab [<t>]": Key("cs-tab:%(t)d"),

        "Denny triage": Text("cd /usr/share/indeni-knowledge/stable/automation") + Key("enter"),
        "Ansible logs": Text("cd /usr/share/indeni-services/logs/ansible") + Key("enter"),
        "Denny knowledge": Text("cd /usr/share/indeni-knowledge") + Key("enter"),
        "Denny server": Text("cd /usr/share/indeni") + Key("enter"),
        "Denny collector": Text("cd /usr/share/indeni") + Key("enter"),

        "restart server": Text("sudo res") + Key("enter"),
        "stop server": Text("sudo res stop") + Key("enter"),
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



mobaxterm_context = AppContext(executable='mobaxterm')
mobaxterm_grammar = Grammar('MobaXterm', context=mobaxterm_context)
mobaxterm_grammar.add_rule(MobaXtermMapping())
mobaxterm_grammar.load()

def unload():
    global mobaxterm_grammar
    mobaxterm_grammar = utils.unloadHelper(mobaxterm_grammar, __name__)
