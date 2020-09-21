import os, webbrowser

from dragonfly import *
from dragonfly.actions.action_base import BoundAction
from dragonfly.engines import get_engine

from supporting import utils, character

def openSite(letters_ref):
    print character.CHARACTER_MAP[letters_ref].upper()

class Example(MappingRule):
    letters = List("letters_list", [
                       character.A, character.B, character.C, character.D, character.E, character.F, character.G, character.H, character.I, character.J, character.K, character.L, character.M, character.N, character.O, character.P, character.Q, character.R, character.S, character.T, character.U, character.V, character.W, character.X, character.Y, character.Z
                   ])

    #element = Sequence([Literal("item"), ])
    mapping = {
        "Dirk donk doitey <letters_ref>": Function(openSite)
    }
    extras = [ListRef("letters_ref", letters)]
    # extras = [Dictation("dictation"),
    #           Integer("w", 0, 10),
    #           Integer("x", 0, 9),
    #           Integer("y", 0, 9),
    #           Integer("z", 0, 9),
    #           ]
    # defaults = {"dictation":None}


example_grammar = Grammar("example grammar")
example_grammar.add_rule(Example())


example_grammar.load()

def unload():
    global example_grammar
    example_grammar = utils.unloadHelper(example_grammar, __name__)