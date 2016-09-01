from dragonfly import *

import _b

def printCharlie(): print "charlie"
def printFoxtrot(): print "foxtrot"
class CharlieMap(MappingRule):
    mapping = {
        "print charlie": Function(printCharlie),
    }



alternatives = []
alternatives.append(RuleRef(rule=CharlieMap()))
alternatives.append(RuleRef(rule=_b.BravoMap()))

single_action = Alternative(alternatives)

sequence = Repetition(single_action, min=1, max=16, name="sequence")


class ChainRule(CompoundRule):
    spec = "<sequence>"
    extras = [
        sequence, # Sequence of actions defined above.
    ]

    #  - node -- root node of the recognition parse tree.
    #  - extras -- dict of the "extras" special elements:
    #     . extras["sequence"] gives the sequence of actions.
    def _process_recognition(self, node, extras):
        sequence = extras["sequence"]   # A sequence of actions.
        # print "sequence: " + str(sequence)
        action_loop_count = -1
        for action in sequence:
            # print "action: " + str(action)
            # print "node words: " + str(node.words())
            action.execute()



grammar = Grammar("example grammar")
grammar.add_rule(ChainRule())

grammar.load()

def unload():
    print "unloading...."
    #reload(_working)
    global grammar
    if grammar: grammar.unload()
    grammar = None
