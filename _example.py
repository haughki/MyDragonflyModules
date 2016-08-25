# import sys
# sys.path.append('pycharm-debug.egg')
# import pydevd
# pydevd.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)



from dragonfly import *
from natlinkmain import micOnCallback
from hawk import utils


def reloader():
    print "reloading..."
    micOnCallback()
    utils.touch("C:\\NatLink\\NatLink\MacroSystem\\_c.py")
    micOnCallback()

class ExampleMapping(MappingRule):
    mapping = {
        "execute reload": Function(reloader),
    }
    extras = [
        Dictation("text"),
    ]


import logging
rule_log = logging.getLogger("rule")

class ExampleRule(CompoundRule):
    spec = "silly"                  # Spoken form of command.

    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        Key("alt:up,s-down").execute()
        






grammar = Grammar("example grammar")
grammar.add_rule(ExampleRule())
grammar.add_rule(ExampleMapping())


grammar.load()

def unload():
    #reload(_working)
    global grammar
    if grammar: grammar.unload()
    grammar = None
