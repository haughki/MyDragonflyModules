from dragonfly import (Grammar, AppContext, MappingRule, Integer, Key, Text, Mimic, Dictation, Function, CompoundRule,
                       Pause)

release = Key("alt:up, shift:up, ctrl:up")

class AlternateKeyMap(MappingRule):
    mapping = {
        "wave": Key("shift:up, right"),
        #        "boss": Key("ctrl:down"),
        #        "shun": Key("ctrl:up"),
        "switch": release + Key("ctrl:down, tab"),
        "show apps": release + Key("alt:down, tab"),
        "mimic <text>": release + Mimic(extra="text"),
        "pop": Key("apps"), # right click
        "list Windows": Mimic("list", "all", "Windows"),

        ### programming
        "short object": Text("obj"),
        "short string": Text("str"),
        "jason": Text("json"),

        ### Dragonfly Commands
        "add text map": Text("\"\": Text(\"\"),") + Key("left:12"),
        "add key map": Text("\"\": Key(\"\"),") + Key("left:11"),

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

multiedit_alternate_grammar = Grammar("Multiedit Alternate")
multiedit_alternate_grammar.add_rule(AlternateKeyMap())
multiedit_alternate_grammar.load()

def unload():
    global multiedit_alternate_grammar
    if multiedit_alternate_grammar:
        print "unloading " + __name__ + "..."
        multiedit_alternate_grammar.unload()
    multiedit_alternate_grammar = None