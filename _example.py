# import sys
# sys.path.append('pycharm-debug.egg')
# import pydevd
# pydevd.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)



from dragonfly import *

from supporting import utils, character



class Example(MappingRule):
    mapping = {
        "Dirk": Key("d"),
    }

    extras = [Dictation("dictation_to_find"),
              ]
    defaults = {"dictation_to_find":""}


example_grammar = Grammar("example grammar")
example_grammar.add_rule(Example())


example_grammar.load()

def unload():
    global example_grammar
    if example_grammar:
        print "unloading " + __name__ + "..."
        example_grammar.unload()
    example_grammar = None
