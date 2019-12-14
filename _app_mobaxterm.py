"""A command module for Dragonfly, for controlling VSCode.
-----------------------------------------------------------------------------
Licensed under the LGPL3.

"""

from dragonfly import Grammar, MappingRule, Dictation, Integer, Key, Text, IntegerRef, AppContext, Pause, Mouse
from supporting import utils


#---------------------------------------------------------------------------
# Shortcuts
#---------------------------------------------------------------------------

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


# def getFile(text=None):
#     open_get_file_dialog = Key("c-p")
#     if text:
#         open_get_file_dialog.execute()
#         file_name = str(text).lower()
#         Text(file_name).execute()
#     else:
#         open_get_file_dialog.execute()
#
# def printNumber(w, x=None, y=None, z=None):
#     number = utils.buildNumber(w, x, y, z)
#     Text(number).execute()

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


        "short list": Text("ls") + Key("enter"),
        "go home": Text("cd ~") + Key("enter"),
        "clear line": Key("c-a") + Key("c-k") + Key("enter"),
        "to Jason": Text(" | python -m json.tool") + Key("enter"),



        "cat": T("cat "),
        "Clyde copy": T("cp "),
        "chai": T("cd "),
        "chai <text>": T("cd %(text)s") + K("tab,enter"),
        "chai chain <text>": T("cd %(text)s") + K("tab:3"),
        "chain <text>": T("%(text)s") + K("tab:3"),
        "chai up": T("cd ..\n"),
        # "chaif <common_folder>": T("cd %(common_folder)s\n"),
        "echo": T("echo "),
        "echo path": T("echo $PATH\n"),
        "environment": T("env\n"),
        # "<grep>": T("%(grep)s -rin -B2 -A2 '' .") + K("left:3"),
        # "<grep> <text>": T("%(grep)s -rin -B2 -A2 '%(text)s' .\n"),
        "grep": T("grep -rin -B2 -A2 '' .") + K("left:3"),
        "grep <text>": T("grep -rin -B2 -A2 '%(text)s' .\n"),
        "info documentation": T("info "),
        "jobs": T("jobs -l\n"),
        "jobs running": T("jobs -lr\n"),
        "jobs stopped": T("jobs -ls\n"),
        "list": T("ls -la\n"),
        "list <text>": T("ls -la %(text)s") + K("tab,enter"),
        "list chain <text>": T("ls -la %(text)s") + K("tab:3"),
        "list up": T("ls -la ..\n"),
        "list up up": T("ls -la ../..\n"),
        "locate": T("locate "),
        "man page": T("man "),
        "chai chai": T("mkdir "),
        "chai chai <text>": T("mkdir %(text)s\n"),
        "chai chai parent": T("mkdir -p "),
        "chai chai parent <text>": T("mkdir -p %(text)s\n"),
        "move": T("mv "),
        "move <text> to [<text2>]": T("mv %(text)s") + K("tab") + T(" %(text2)s") + K("tab"),
        "push (directory | chai)": T("pushd .\n"),
        "push other (directory | chai)": T("pushd "),
        "pop (directory | chai)": T("popd\n"),
        "(directory | chai) stack": T("dirs\n"),
        "print (working directory | chai)": T("pwd\n"),
        "remove": T("rm "),
        "remove (directory | chai)": T("rmdir "),
        "remove (directory | chai) recursively": T("rmdir -r"),
        "run": T("./"),
        "run <text>": T("./%(text)s") + K("tab,enter"),
        "(sudo | super [user] do)": T("sudo "),
        "switch user": T("su "),
        "time": T("time "),
        "who am I": T("whoami\n"),
        "help flag": T(" --help"),
        "help flag short": T(" -h"),
        "verbose flag": T(" --verbose"),
        "verbose flag short": T(" -v"),
        # tools
        "apt[itude] search": T("sudo aptitude search "),
        "apt[itude] install": T("sudo aptitude install "),
        "apt[itude] show": T("sudo aptitude show "),
        "apt[itude] update": T("sudo aptitude update\n"),
        "apt[itude] upgrade": T("sudo aptitude update && aptitude upgrade\n"),
        "web get": T("wget "),
        "vim": T("vim "),
        "vim <text>": T("vim %(text)s") + K("tab,enter"),
        "suvim": T("sudo vim "),
        "suvim <text>": T("sudo vim %(text)s") + K("tab,enter"),


        # #"[go to | show] project window": Key("a-1"),
        #
        # # Search.
        # "replace": Key("c-r"),
        # "show find": Key("c-f"),
        # "find <text>": Key("c-f/25") + Text("%(text)s"),
        # # "find next": Key("f3"),
        # # "find (prev | previous)": Key("s-f3"),
        # # "find in files": Key("cs-f"),
        #
        # # Edit.
        # "[shoreline | show] line <w> [<x>] [<y>] [<z>]": Key("c-g/25") + Function(printNumber)+ Key("enter"),
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



context = AppContext(executable='mobaxterm')
mobaxterm_grammar = Grammar('MobaXterm', context=context)
mobaxterm_grammar.add_rule(MobaXtermMapping())
mobaxterm_grammar.load()

def unload():
    global mobaxterm_grammar
    mobaxterm_grammar = utils.unloadHelper(mobaxterm_grammar, __name__)
