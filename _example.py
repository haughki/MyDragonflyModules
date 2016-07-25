from dragonfly import *


# class ExampleMapping(MappingRule):
#     """ This mimics the "switch to" command from DNS to use the Dragonfly "focus" command syntax.
#     The main definitions of the Dragonfly "focus" command are in _winctrl.py.
#     """
#     mapping = {
#         "web search <text>": Mimic("search", "the", "web", "for", extra="text"),
#     }
#     extras = [
#         Dictation("text"),
#     ]
#
#
# # Create a grammar which contains and loads the command rule.
# grammar = Grammar("Testing")
# grammar.add_rule(ExampleMapping())


# import sys
# sys.path.append('pycharm-debug.egg')
# import pydevd
# pydevd.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)


import logging

from dragonfly import log

log.setup_log()
# log.setup_tracing()

class ExampleRule(CompoundRule):
    spec = "Dirk"                  # Spoken form of command.

    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        print 'found Dirk'
        print node.words()

        focusIdea = FocusWindow("idea")
        focusIdea.execute()


#Create a grammar which contains and loads the command rule.
dirk_rule = ExampleRule()
grammar = Grammar("example grammar")
grammar.add_rule(dirk_rule)


grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
