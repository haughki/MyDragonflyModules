from dragonfly import (Grammar, MappingRule, Integer, Key, Text, Mimic, Dictation, Pause)

from supporting import utils

release = Key("alt:up, shift:up, ctrl:up, win:up")

class MultiMoreKeyMap(MappingRule):
    mapping = {
        "wave": Key("shift:up, right"),
        #        "boss": Key("ctrl:down"),
        #        "shun": Key("ctrl:up"),
        "switch": release + Key("ctrl:down, tab"),
        "show [all] apps | show [all] Windows": release + Key("alt:down, tab"),
        "mimic <text>": release + Mimic(extra="text"),
        "pop": Key("apps"), # right click
        "focus chrome too": Mimic("focus", "chrome") + Pause("25") + Mimic("focus", "chrome"),

        # Dragon NaturallySpeaking mimics
        "list Windows": Mimic("list", "all", "Windows"),
        "(web search | search web) <text>": Mimic("search", "the", "web", "for", extra="text"),

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

multiedit_more_grammar = Grammar("Multiedit More")
multiedit_more_grammar.add_rule(MultiMoreKeyMap())
multiedit_more_grammar.load()

def unload():
    global multiedit_more_grammar
    multiedit_more_grammar = utils.unloadHelper(multiedit_more_grammar, __name__)