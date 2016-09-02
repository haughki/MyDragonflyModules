# import sys
# sys.path.append('pycharm-debug.egg')
# import pydevd
# pydevd.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)



from dragonfly import *

from supporting import utils

class Example(CompoundRule):
    spec = "find object"

    def _process_recognition(self, node, extras):
        an_id = 202945552
        found = utils.objects_by_id(an_id)
        if found:
            print found
        else:
            print "None"


example_grammar = Grammar("example grammar")
example_grammar.add_rule(Example())


example_grammar.load()

def unload():
    global example_grammar
    if example_grammar:
        print "unloading " + __name__ + "..."
        example_grammar.unload()
    example_grammar = None
