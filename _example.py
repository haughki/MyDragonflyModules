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
    """ This mimics the "switch to" command from DNS to use the Dragonfly "focus" command syntax.
    The main definitions of the Dragonfly "focus" command are in _winctrl.py.
    """
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
        print node.words()
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
