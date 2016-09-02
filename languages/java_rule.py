# import sys
# sys.path.append('pycharm-debug.egg')
# import pydevd
# pydevd.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)
from dragonfly import Dictation
from dragonfly import Function
from dragonfly import Key, Text, MappingRule

from languages import specs


def defineMethod(modifiers=None):
    if modifiers is None:
        modifiers = "private"
    else:
        modifiers = str(modifiers).lower()

    Text(modifiers + " void a()").execute()
    Key("enter, lbrace, enter, up:2, ctrl:down, right:" + str(
        len(modifiers.split(" ")) + 1) + ", ctrl:up, del").execute()

class JavaRule(MappingRule):

    mapping = {
        "deco override":                            Text("@Override"),
        "line comment":                             Text("// "),
        specs.SymbolSpecs.IF:                       Text("if(){") + Key("enter,up,left"),
        specs.SymbolSpecs.ELSE:                     Text("else {") + Key("enter"),
        specs.SymbolSpecs.DEFINE_METHOD:            Function(defineMethod),
        specs.SymbolSpecs.FOR_EACH_LOOP:            Text("for( : ){") + Key("enter,up,left:4"),
        specs.SymbolSpecs.SYSOUT:                   Text("System.out.println()")+Key("left"),
    }
    extras = [
        Dictation("modifiers"),
    ]
    defaults = {
        "modifiers": None,
    }

