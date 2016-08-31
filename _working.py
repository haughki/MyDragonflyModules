# import sys
# sys.path.append('pycharm-debug.egg')
# import pydevd
# pydevd.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)



from dragonfly import *
from natlinkmain import micOnCallback
from supporting import utils




def something():
    print "something to see..."

class ExampleMapping(MappingRule):
    mapping = {
        "execute something": Function(something),
    }
    extras = [
        Dictation("text"),
    ]

example = ExampleMapping()


def disable():
    example.disable()
    
class Disabler(MappingRule):
    mapping = {
        "disable example": Function(disable)
    }



grammar = Grammar("example grammar")
grammar.add_rule(example)
grammar.add_rule(Disabler())
grammar.load()



def unload():
    #reload(_working)
    global grammar
    if grammar: grammar.unload()
    grammar = None
