"""A command module for Dragonfly, for controlling notepad++.
-----------------------------------------------------------------------------
Licensed under the LGPL3.

"""

from dragonfly import Grammar, MappingRule, Dictation, Integer, Key, Text, IntegerRef, AppContext, Function
from supporting import utils

def getFile(text=None):
    open_get_file_dialog = Key("c-p")
    if text:
        open_get_file_dialog.execute()
        file_name = str(text).lower()
        Text(file_name).execute()
    else:
        open_get_file_dialog.execute()

def printNumber(w, x=None, y=None, z=None):
    number = utils.buildNumber(w, x, y, z)
    Text(number).execute()

class VsCodeMapping(MappingRule):
    mapping = {
        #"[go to | show] project window": Key("a-1"),

        # Search.
        "replace": Key("c-r"),
        "show find": Key("c-f"),
        "find <text>": Key("c-f/25") + Text("%(text)s"),
        # "find next": Key("f3"),
        # "find (prev | previous)": Key("s-f3"),
        # "find in files": Key("cs-f"),

        # Code.
        "[shoreline | show] line <w> [<x>] [<y>] [<z>]": Key("c-g/25") + Function(printNumber)+ Key("enter"),
        "[show] white space": Key("cs-w"),
        "word wrap": Key("cs-d"),

        # Code navigation.
        "get file [<text>]": Function(getFile),  # "Navigate > File..."
        "toggle (book | bookmark)": Key("f7"),
        "next (book | bookmark)": Key("cs-n"),
        "(prev | previous) book": Key("cs-p"),

        # Window handling.
        "new tab": Key("c-n"),
        "next tab [<t>]": Key("c-pagedown:%(t)d"),
        "(preev | previous) tab [<t>]": Key("c-pageup:%(t)d"),
        "close tab": Key("c-w"),
        "(full-screen | full screen)": Key("cs-x"),
        "side panel": Key("c-b"),
    }
    extras = [
        Integer("t", 1, 50),
        Dictation("text"),
        IntegerRef("n", 1, 50000),
        Integer("w", 0, 10),
        Integer("x", 0, 10),
        Integer("y", 0, 10),
        Integer("z", 0, 10)
    ]
    defaults = {
        "t": 1,
    }


context = AppContext(executable='code')
vscode_grammar = Grammar('VsCode', context=context)
vscode_grammar.add_rule(VsCodeMapping())
vscode_grammar.load()

def unload():
    global vscode_grammar
    vscode_grammar = utils.unloadHelper(vscode_grammar, __name__)
