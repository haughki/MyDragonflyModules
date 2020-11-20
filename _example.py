import os, webbrowser

from dragonfly import *
from dragonfly.actions.action_base import BoundAction
from dragonfly.engines import get_engine

from supporting import utils, character
from ccr import basechainrule

class Example(MappingRule):
    mapping = {
        "Dirk donk": Text("dirk donker dude"),
        "boink": Text("boinker"),
    }
    # extras = [Dictation("dictation"),
    #           Integer("w", 0, 10),
    #           Integer("x", 0, 9),
    #           Integer("y", 0, 9),
    #           Integer("z", 0, 9),
    #           ]
    # defaults = {"dictation":None}

class Example2(MappingRule):
    mapping = {
        "slug monkey": Text("the slug and the monkey"),
        "zapper": Text("zip zap"),
    }

alternatives = [
    RuleRef(rule=Example()),
    RuleRef(rule=Example2()),
]



example_grammar = Grammar("example grammar")
example_grammar.add_rule(basechainrule.BaseChainRule(alternatives))


example_grammar.load()

def unload():
    global example_grammar
    example_grammar = utils.unloadHelper(example_grammar, __name__)