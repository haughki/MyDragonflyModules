from dragonfly import *

import _continuous_rec_import

def printKilo(): print "kilo"
def printLima(): print "lima"
class KiloMap(MappingRule):
    mapping = {
        "print kilo": Function(printKilo()),
    }



alternatives = []
alternatives.append(RuleRef(rule=KiloMap()))
alternatives.append(RuleRef(rule=_continuous_rec_import.TangoMap()))

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
        for action in sequence:
            # print "action: " + str(action)
            # print "node words: " + str(node.words())
            action.execute()



chain_grammar = Grammar("chain grammar")
chain_grammar.add_rule(ChainRule())

chain_grammar.load()

def unload():
    print "unloading...."
    global chain_grammar
    if chain_grammar: chain_grammar.unload()
    chain_grammar = None
