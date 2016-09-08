# import sys
# sys.path.append('pycharm-debug.egg')
# import pydevd
# pydevd.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)
import os

from dragonfly import *
from dragonfly.actions.action_base import BoundAction

from supporting import utils, character

def defineMethod(_node):
    # "define [(public | protected | private)] [static] [void] method"
    modifiers_string = None
    if len(_node.words()) > 2:
        modifiers = _node.words()[1: -1]
        modifiers_string = ""
        for modifier in modifiers:
            modifiers_string = modifiers_string + modifier + " "




    # method_index = -1
    # for i in range(len(command)):
    #     if command[i] == "method":
    #         method_index = i
    #     
    # if method_index > 1:

class Example(MappingRule):
    mapping = {
        "Dirk [(public | protected | private)] [static] [void] method": Function(defineMethod),
    }
    extras = [Dictation("dictation")]


example_grammar = Grammar("example grammar")
example_grammar.add_rule(Example())


example_grammar.load()

def unload():
    global example_grammar
    if example_grammar:
        print "unloading " + __name__ + "..."
        example_grammar.unload()
    example_grammar = None
