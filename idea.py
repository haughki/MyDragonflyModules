"""A command module for Dragonfly, for controlling IntelliJ IDEA-based IDEs.

taken from nirvdrum's module at:
https://github.com/dictation-toolbox/dragonfly-scripts/blob/master/_app_intellij.py
-----------------------------------------------------------------------------
Licensed under the LGPL3.

"""

from dragonfly import Grammar, MappingRule, Dictation, Integer, Key, Text, IntegerRef, AppContext

class CommandRule(MappingRule):
    mapping = {
        # Code execution.
        "run app": Key("s-f10"),
        "re-run app": Key("c-f5"),
        "run test": Key("cs-f10"),
        "stop running": Key("c-f2"),

        # Code navigation.
        # "navigate to class <text>": Key("c-n") + Pause("30") + Function(lib.format.pascal_case_text) + Pause("30") + Key("enter"),
        # "navigate to class chooser <text>": Key("c-n") + Pause("30") + Function(lib.format.pascal_case_text) + Pause("30"),
        # "navigate to file <text>": Key("cs-n") + Pause("30") + Function(lib.format.camel_case_text) + Pause("30") + Key("enter"),
        # "navigate to file chooser <text>": Key("cs-n") + Pause("30") + Function(lib.format.camel_case_text) + Pause("30"),
        # "navigate to symbol <text>": Key("cas-n") + Pause("30") + Function(lib.format.camel_case_text) + Pause("30") + Key("enter"),
        # "navigate to symbol chooser <text>": Key("cas-n") + Pause("30") + Function(lib.format.camel_case_text) + Pause("30"),
        "[go to | show] declaration": Key("c-b"),
        "[go to | show] implementation": Key("ca-b"),
        "[go to | show] super": Key("c-u"),
        "[go to | show] (class|test)": Key("cs-t"),
        # "go back": Key("ca-left"), Key("as-left"),

        # Project settings.
        "[go to | show] project window": Key("a-1"),
        "[go to | show] module settings": Key("f4"),
        "[go to | show] [project] settings": Key("ca-s"),
        "synchronize files": Key("ca-y"),

        # Terminal.
        "run terminal": Key("a-f12"),

        # Search.
        'find <text>': Key("c-f/25") + Text("%(text)s"),
        'find next': Key('f3'),
        'find (prev | previous)': Key('s-f3'),
        "find in files": Key("cs-f"),
        # "find usages": DynamicAction(Key("a-f7"), Key("as-7")),

        # Code.
        "show intentions": Key("a-enter"),
        "accept choice": Key("c-enter"),
        "implement method": Key("c-i"),
        "override method": Key("c-o"),

        # Edit
        "[go to | show] line <n>": Key("c-g/25") + Text("%(n)d") + Key("enter"),
        "(full-screen | full screen)": Key("cs-x"),
        "comment [line | that | it]": Key("c-slash"),

        # Window handling.
        "next tab [<t>]": Key("a-right/5:%(t)d"),
        "(preev | previous) tab [<t>]": Key("a-left/5:%(t)d"),
        "close tab": Key("c-w"),

        # Version control.
        "show diff": Key("c-d"),

        # Refactoring.
        "(refactor|re-factor) (this|choose)": Key("cas-t"),
        "(refactor|re-factor) rename": Key("s-f6"),
        "(refactor|re-factor) change signature": Key("c-f6"),
        "(refactor|re-factor) move": Key("f6"),
        "(refactor|re-factor) copy": Key("f5"),
        "(refactor|re-factor) safe delete": Key("a-del"),
        "(refactor|re-factor) extract variable": Key("ca-v"),
        "(refactor|re-factor) extract constant": Key("ca-c"),
        "(refactor|re-factor) extract field": Key("ca-f"),
        "(refactor|re-factor) extract parameter": Key("ca-p"),
        "(refactor|re-factor) extract variable": Key("ca-v"),
        "(refactor|re-factor) extract method": Key("ca-m"),
        "(refactor|re-factor) (in line|inline)": Key("ca-n"),

        # Custom key mappings.
        "(run SSH session|run SSH console|run remote terminal|run remote console)": Key("a-f11/25, enter"),
    }
    extras = [
        Integer("t", 1, 50),
        Dictation("text"),
        IntegerRef("n", 1, 50000)
    ]
    defaults = {
        "t": 1,
    }


context = AppContext(executable='idea')
grammar = Grammar('IntelliJ Idea', context=context)

grammar.add_rule(CommandRule())
grammar.load()

# Unload function which will be called by natlink at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None