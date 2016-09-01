# import sys
# sys.path.append('pycharm-debug.egg')
# import pydevd
# pydevd.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)



from dragonfly import *
import _a
import _b

def enableAlpha():
    print "enabling alpha"
    _a.alpha_rule.enable()

def disableAlpha():
    print "disabling alpha"
    _a.alpha_rule.disable()

def enableBravo():
    print "enabling bravo"
    _b.bravo_rule.enable()

def disableBravo():
    print "disabling bravo"
    _b.bravo_rule.disable()


class ExampleMapping(MappingRule):
    mapping = {
        "enable alpaha": Function(enableAlpha),
        "disable alpaha": Function(disableAlpha),
        "enable bravo": Function(enableBravo),
        "disable bravo": Function(disableBravo),
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
