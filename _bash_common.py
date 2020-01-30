"""A command module for Dragonfly, for controlling VSCode.
-----------------------------------------------------------------------------
Licensed under the LGPL3.

"""

from dragonfly import Grammar, MappingRule, Dictation, Integer, Key, Text, IntegerRef, AppContext, Pause, Mouse, Function
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

def printUpDir(w):
    cd_command = "cd "
    for i in range(w):
        cd_command += "../"
    Text(cd_command).execute()


class BashCommonMapping(MappingRule):
    mapping = {
        "short list": Text("ls") + Key("enter"),
        "go home": Text("cd ~") + Key("enter"),
        "[clear | free] line": Key("c-a") + Key("c-k"),
        "free arg[ument]": Key("c-w"),
        "to Jason": Text(" | python -m json.tool") + Key("enter"),

        "swat": Key("c-w"),



        "cat": T("cat "),
        "Clyde copy": T("cp "),
        "chai": T("cd "),
        "chai <text>": T("cd %(text)s") + K("tab,enter"),
        "chai chain <text>": T("cd %(text)s") + K("tab:3"),
        "chain <text>": T("%(text)s") + K("tab:3"),
        "chai up": T("cd ..\n"),
        "chai up [<w>]": Function(printUpDir),  # + Key("enter")
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
        "make dir[ectory]": T("mkdir "),
        "make dir[ectory] <text>": T("mkdir %(text)s\n"),
        "make dir[ectory] parent": T("mkdir -p "),
        "make dir[ectory] parent <text>": T("mkdir -p %(text)s\n"),
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

        # checkpoint
        "clish command": T("clish -c \"\"") + K("left")
    }

    extras = [
        Integer("t", 1, 50),
        Dictation("text"),
        Dictation("text2"),
        IntegerRef("n", 1, 50000),
        Integer("w", 1, 10),
        # Integer("x", 0, 10),
        # Integer("y", 0, 10),
        # Integer("z", 0, 10)
    ]
    defaults = {
        "t": 1,
        "text": "",
        "text2": ""
    }


ubu_context = AppContext(executable='ubuntu')
moba_context = AppContext(executable='mobaxterm')
mintty_context = AppContext(executable='mintty')  # git bash, git for Windows
multi_context = ubu_context | moba_context | mintty_context
bash_common_grammar = Grammar('BashCommon', context=multi_context)
bash_common_grammar.add_rule(BashCommonMapping())
bash_common_grammar.load()

def unload():
    global bash_common_grammar
    bash_common_grammar = utils.unloadHelper(bash_common_grammar, __name__)
