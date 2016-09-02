# import sys
# sys.path.append('pycharm-debug.egg')
# import pydevd
# pydevd.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)
from dragonfly import Dictation
from dragonfly import Key, Text, MappingRule

from languages import specs


class PythonRule(MappingRule):
    mapping = {
            "(shells | else) if":                   Key("e,l,i,f,space,colon,left"),
            specs.SymbolSpecs.IF:                   Key("i,f,space,colon,left"),
            specs.SymbolSpecs.ELSE:                 Text("else:") + Key("enter"),
            specs.SymbolSpecs.DEFINE_METHOD:        Text("def (self):") + Key("left:7"),
            specs.SymbolSpecs.FOR_LOOP:             Text("for i in range(0, ):") + Key("left:2"),
            specs.SymbolSpecs.FOR_EACH_LOOP:        Text("for in :") + Key("left:4"),
            specs.SymbolSpecs.SYSOUT:               Text("print "),
            specs.SymbolSpecs.TO_STRING:            Text("str()")+ Key("left"),
    }            
    extras = [
        Dictation("modifiers"),
    ]
    defaults = {
        "modifiers": None,
    }
