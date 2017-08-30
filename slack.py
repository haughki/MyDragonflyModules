from dragonfly import (Grammar, AppContext, MappingRule, Integer, Key, Text, Dictation)


class SlackMapping(MappingRule):
    mapping = {
        # "new (thing | tab)": Key("c-t"),
        # "new window": Key("c-n"),
        # "reopen tab": Key("cs-t"),
        # "(next | nex) (tab | ab) [<n>]": Key("c-pgdown:%(n)d"),
        # "(previous | preev) tab [<n>]": Key("c-pgup:%(n)d"),
        # "show tab <tab>": Key("c-%(tab)d"),
        "switch <text>": Key("c-k/25") + Text("%(text)s") + Key("enter"),

        # "open <w> [<x>] [<y>] [<z>]": Key("cs-space/" + click_by_voice_delay) + Function(printNumber) + Key("enter"),  # click by voice
        # "open focus <w> [<x>] [<y>] [<z>]": Key("cs-space/" + click_by_voice_delay) + Function(printNumberFocus) + Key("enter"),  # click by voice
    }
    extras=[
        Integer("n", 1, 50),
        Integer("number", 1, 9999),
        Dictation("text"),
    ]
    defaults = {
        "n": 1,
    }



context = AppContext(executable="slack")
slack_grammar = Grammar("Slack", context=context)
slack_grammar.add_rule(SlackMapping())
slack_grammar.load()

def unload():
    global slack_grammar
    if slack_grammar:
        print "unloading " + __name__ + "..."
        slack_grammar.unload()
    slack_grammar = None
