import os, webbrowser

from dragonfly import *
from dragonfly.actions.action_base import BoundAction

from supporting import utils, character

def openSite():
    webbrowser.open("https://drive.google.com/drive/my-drive")


class Example(MappingRule):
    mapping = {
        "Dirk": Function(openSite)
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
