"""
copied from: https://github.com/codebold/hiccup/blob/master/rules/choices/base.py
"""

# from actions.action_shortcut import (
#     K,
#     T,
#     M
# )

from dragonfly import MappingRule, Dictation
# import choices.base as chc_base


from dragonfly import (Text, Key, Pause, Mouse, AppContext, Grammar)

from supporting import utils


#---------------------------------------------------------------------------
# Shortcuts
#---------------------------------------------------------------------------

def T(s, pause=0.00001, **kws):
    return Text(s, pause=pause, **kws)

def K(*args, **kws):
    return Key(*args, **kws)

def P(*args, **kws):
    return Pause(*args, **kws)

def M(*args, **kws):
    return Mouse(*args, **kws)

# ---------------------------------------------------------------------------
# Core Rule
# ---------------------------------------------------------------------------

class ShellCoreRule(MappingRule):
    mapping = {
        "get out": K(),
        "exit": T("exit\n"),
        "alias": T("alias "),
        "cat": T("cat "),
        "shell copy": T("cp "),
        "chai": T("cd "),
        "chai <text>": T("cd %(text)s") + K("tab,enter"),
        "chai chain <text>": T("cd %(text)s") + K("tab:3"),
        "chain <text>": T("%(text)s") + K("tab:3"),
        "chai up": T("cd ..\n"),
        # "chaif <common_folder>": T("cd %(common_folder)s\n"),
        "differences": T("diff "),
        "disk usage": T("du -ch\n"),
        "disk usage all": T("du -ach\n"),
        "echo": T("echo "),
        "echo path": T("echo $PATH\n"),
        "environment": T("env\n"),
        "glimpse": T("glimpse "),
        # "<grep>": T("%(grep)s -rin -B2 -A2 '' .") + K("left:3"),
        # "<grep> <text>": T("%(grep)s -rin -B2 -A2 '%(text)s' .\n"),
        "info documentation": T("info "),
        "jobs": T("jobs -l\n"),
        "jobs running": T("jobs -lr\n"),
        "jobs stopped": T("jobs -ls\n"),
        "kill process": T("kill "),
        "kill process now": T("kill -9 "),
        "link soft": T("ln -s "),
        "link hard": T("ln "),
        "list": T("ls -la\n"),
        "list <text>": T("ls -la %(text)s") + K("tab,enter"),
        "list chain <text>": T("ls -la %(text)s") + K("tab:3"),
        "list up": T("ls -la ..\n"),
        "list up up": T("ls -la ../..\n"),
        "locate": T("locate "),
        "locate update": T("updatedb\n"),
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
        # "switch user <os_user>": T("su %(os_user)s\n"),
        "time": T("time "),
        "user mask": T("umask "),
        "who am I": T("whoami\n"),
        "help flag": T(" --help"),
        "help flag short": T(" -h"),
        "verbose flag": T(" --verbose"),
        "verbose flag short": T(" -v"),
        "run updates": T("runupdates \n"),
        "force updates": T("runupdates -f\n"),
        "check updates": T("checkupdates\n"),
        "restart": T("sudo shutdown -r now\n"),
        "reboot": T("sudo reboot\n"),
        "shutdown": T("sudo shutdown now\n"),
        "shaste": M("(0.5, 0.5), right"),
        # tools
        "apt[itude] search": T("sudo aptitude search "),
        "apt[itude] install": T("sudo aptitude install "),
        "apt[itude] show": T("sudo aptitude show "),
        "apt[itude] update": T("sudo aptitude update\n"),
        "apt[itude] upgrade": T("sudo aptitude update && aptitude upgrade\n"),
        "gem[s] chek": T("gem outdated\n"),
        "gem[s] update": T("gem update\n"),
        "MD 5 check": T("md5sum -c "),
        "root kit Hunter check": T("rkhunter --check\n"),
        "root kit Hunter update": T("rkhunter --propupd\n"),
        "check root kit": T("chkrootkit\n"),
        "web get": T("wget "),
        # "vim": T("vi "),
        # "vim <text>": T("vi %(text)s") + K("tab,enter"),
        # "vimf <common_file>": T("vi %(common_file)s\n"),
        # "vimslap": T("vi\n"),
        # "suvim": T("sudo vi "),
        # "suvim <text>": T("sudo vi %(text)s") + K("tab,enter"),
        # "suvimf <common_file>": T("sudo vi %(common_file)s\n"),
        # "suvimslap": T("sudo vi\n"),
        # "emacs": T("emacs "),
        # "emacs <text>": T("emacs %(text)s") + K("tab,enter"),
        # "emaff <common_file>": T("emacs %(common_file)s\n"),
        # "emacslap": T("emacs\n"),
        # "sumacs": T("sudo emacs "),
        # "sumacs <text>": T("sudo emacs %(text)s") + K("tab,enter"),
        # "sumaff <common_file>": T("sudo emacs %(common_file)s\n"),
        # "sumacslap": T("sudo emacs\n"),
    }
    defaults = {
        "text": "",
        "text2": ""
    }
    extras = [
        Dictation("text"),
        Dictation("text2"),
        # chc_base.common_file,
        # chc_base.common_folder,
        # chc_base.grep,
        # chc_base.os_user
    ]




# context = AppContext(executable="virtualbox", title="ubuntu-desktop-amd64")
context = AppContext(executable="virtualbox")
shell_grammar = Grammar("Linux Shell Grammar", context=context)
shell_grammar.add_rule(ShellCoreRule())
shell_grammar.load()

def unload():
    global shell_grammar
    shell_grammar= utils.unloadHelper(shell_grammar,__name__)