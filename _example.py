# import sys
# sys.path.append('pycharm-debug.egg')
# import pydevd
# pydevd.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)
import os

from dragonfly import *
from dragonfly.actions.action_base import BoundAction

from supporting import utils, character



def buildNumber(w, x=None, y=None, z=None):
    number = str(w)
    if x is not None:
        number += str(x)
    if y is not None:
        number += str(y)
    if z is not None:
        number += str(z)
    Text(number).execute()
        

        
class Example(MappingRule):
    mapping = {
        "Dirk <w> [<x>] [<y>] [<z>]": Function(buildNumber),
    }
    extras = [Dictation("dictation"),
              Integer("w", 0, 10),
              Integer("x", 0, 9),
              Integer("y", 0, 9),
              Integer("z", 0, 9),
              ]
    defaults = {"dictation":None}


example_grammar = Grammar("example grammar")
example_grammar.add_rule(Example())


example_grammar.load()

def unload():
    global example_grammar
    if example_grammar:
        print "unloading " + __name__ + "..."
        example_grammar.unload()
    example_grammar = None
