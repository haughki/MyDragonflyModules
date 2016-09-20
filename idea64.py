"""A command module for Dragonfly, for controlling IntelliJ IDEA-based IDEs.

taken from nirvdrum"s module at:
https://github.com/dictation-toolbox/dragonfly-scripts/blob/master/_app_intellij.py
-----------------------------------------------------------------------------
Licensed under the LGPL3.

"""
from dragonfly import Function
from dragonfly import Grammar, MappingRule, Dictation, Integer, Key, Text, IntegerRef, AppContext

def getFile(text=None):
    open_get_file_dialog = Key("cas-n")
    if text:
        open_get_file_dialog.execute()
        file_name = str(text).lower()
        Text(file_name).execute()
    else:
        open_get_file_dialog.execute()

class CommandRule(MappingRule):
    mapping = {
        # Code execution.
        "run app": Key("s-f10"),
        "debug app": Key("s-f9"),
        "re-run app": Key("c-f5"),
        "run this [app]": Key("cs-f10"),
        "run test": Key("cs-f10"),
        "stop running": Key("c-f2"),
        "[toggle] (breakpoint | break)": Key("c-f8"),
        "step [over]": Key("f8"),
        "step into": Key("f11"),
        "step out": Key("s-f8"),
        "(keep running | resume)": Key("f9"),

        # Code navigation.
        "(go to | show) class": Key("c-n"),
        "get file [<text>]": Function(getFile),  # "Navigate > File..."
        "([go to | show] declaration | dive | plunge)": Key("c-b"),
        "[go to | show] implementation": Key("ca-b"),
        "[go to | show] super": Key("c-u"),
        "float [file] structure": Key("c-f12"),
        "[go to | show] structure": Key("a-7"),
        "[go to | show] hierarchy": Key("a-8"),
        "[go to | show] version control": Key("a-9"),
        "quick definition": Key("cs-i"),
        "quick (documentation | docs)": Key("c-q"),
        "toggle (book | bookmark)": Key("f7"),
        "next (book | bookmark)": Key("cs-n"),
        "(prev | previous) book": Key("cs-p"),
        "expand": Key("c-npadd"),
        "collapse": Key("c-npsub"),

        # Project settings.
        "[go to | show] project [window]": Key("a-1"),
        "[go to | show] module settings": Key("f4"),
        "[go to | show] [project] settings": Key("cas-s"),
        "[go to | show] Global settings": Key("ca-s"),

        # Terminal.
        "run terminal": Key("a-f12"),

        # Search.
        "replace": Key("c-r"),
        "show find": Key("c-f"),
        "find <text>": Key("c-f/25") + Text("%(text)s"),
        "find next": Key("f3"),
        "find (prev | previous)": Key("s-f3"),
        "find in files": Key("cs-f"),
        "find usages": Key("a-f7"),

        # Code.
        "show intentions": Key("a-enter"),
        "accept choice": Key("c-enter"),
        "implement method": Key("c-i"),
        "override method": Key("c-o"),
        "(correct | red light bulb)": Key("a-enter"),
        "show complete": Key("c-space"),
        "context complete": Key("cs-space"),
        "syntax complete": Key("cs-enter"),
        "gets complete": Key("space, equal, space/10, cs-space"),

        # Edit
        "[shoreline | go to | show] (row | line) <n>": Key("c-g/30") + Text("%(n)d") + Key("enter"),
        "(full-screen | full screen)": Key("cs-x"),  # macro, combination of: "Toggle Full Screen Mode" and "Hide All Tool Windows"
        "(Hide | hide | hi) bottom": Key("s-escape"),  # "hide active tool window"
        "(Hide | hide | hi) side": Key("cas-c"),  # "hide side tool windows"
        # "comment [line | that | it]": Key("c-slash"),
        "show white space": Key("cs-w"),
        "redo": Key("cs-z"),
        
        # Window handling.
        "next tab [<t>]": Key("a-right/5:%(t)d"),
        "(preev | previous) tab [<t>]": Key("a-left/5:%(t)d"),
        "close tab": Key("c-w"),

        # Version control.
        "show diff": Key("c-d"),

        # Refactoring.
        "[(refactor|re-factor)] (this|choose)": Key("cas-t"),
        "[(refactor|re-factor)] rename": Key("s-f6"),
        "[(refactor|re-factor)] change signature": Key("c-f6"),
        "[(refactor|re-factor)] move": Key("f6"),
        "[(refactor|re-factor)] copy": Key("f5"),
        "[(refactor|re-factor)] safe delete": Key("a-del"),
        "[(refactor|re-factor)] extract constant": Key("ca-c"),
        "[(refactor|re-factor)] extract field": Key("ca-f"),
        "[(refactor|re-factor)] extract parameter": Key("ca-p"),
        "[(refactor|re-factor)] extract variable": Key("ca-v"),
        "[(refactor|re-factor)] extract method": Key("ca-w"),
        "[(refactor|re-factor)] (in line|inline)": Key("ca-n"),
        
        # Custom key mappings.
        # "(run SSH session|run SSH console|run remote terminal|run remote console)": Key("a-f11/25, enter"),
    }
    extras = [
        Integer("t", 1, 50),
        Dictation("text"),
        IntegerRef("n", 1, 50000)
    ]
    defaults = {
        "t": 1,
    }


context = AppContext(executable="idea64")
grammar = Grammar("IntelliJ Idea", context=context)
grammar.add_rule(CommandRule())
grammar.load()

# Unload function which will be called by natlink at unload time.
def unload():
    global grammar
    if grammar:
        print "unloading " + __name__ + "..."
        grammar.unload()
    grammar = None
