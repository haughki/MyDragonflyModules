# import pydevd_pycharm
# pydevd_pycharm.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)

from dragonfly import Alternative, Repetition, CompoundRule, RuleRef, Grammar
from supporting import utils

from ccr import kilomap, tangomap, compound_test



# This is how to build up alternatives manually:
alternatives = [
    RuleRef(rule=tangomap.TangoMap()),
    RuleRef(rule=kilomap.KiloMap()),
    RuleRef(rule=compound_test.CompoundTestCCR()),
]
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
        print "extras: " + str(extras)
        print "sequence: " + str(sequence)
        print "node words: " + str(node.words())
        print "node: " + str(node)

        for action in extras["sequence"]:
            print "action: " + str(action)
            action.execute()



chain_grammar = Grammar("chain grammar")
chain_grammar.add_rule(ChainRule())

chain_grammar.load()

def unload():
    global chain_grammar
    chain_grammar = utils.unloadHelper(chain_grammar, __name__)
