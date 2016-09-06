import sys
sys.path.append('pycharm-debug.egg')
import pydevd
pydevd.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)



from dragonfly import *
from dragonfly.actions.action_base import BoundAction

from supporting import utils, character



def format_score_function(repeated_choices):
    print repeated_choices
    words = []
    for choice in repeated_choices:
        if isinstance(choice, BoundAction):
            words.append(choice._action._spec)
        else:
            words.append(str(choice))
    print words
    print "_".join(words)

class DirkRule(MappingRule):
    mapping = {
        "Dirk": Text("smirk"),
    }


alternatives = [Dictation("dictation"), RuleRef(rule=DirkRule())]
either_one = Alternative(alternatives)
repeated_choices = Repetition(either_one, min=1, max=16, name="repeated_choices")

class Example(MappingRule):
    mapping = {
        "chore <repeated_choices>": Function(format_score_function)
    }

    extras = [repeated_choices,]
    # defaults = {"dictation":""}



# class ChainRule(CompoundRule):
#     spec = "<action_sequence>"
#     extras = [
#         action_sequence, # action_sequence of actions defined above.
#     ]
# 
#     def _process_recognition(self, node, extras):
#         action_sequence = extras["action_sequence"]   # A action_sequence of actions.
#         # print "action_sequence: " + str(action_sequence)
#         for action in action_sequence:
#             # print "action: " + str(action)
#             # print "node words: " + str(node.words())
#             action.execute()

example_grammar = Grammar("example grammar")
example_grammar.add_rule(Example())


example_grammar.load()

def unload():
    global example_grammar
    if example_grammar:
        print "unloading " + __name__ + "..."
        example_grammar.unload()
    example_grammar = None
