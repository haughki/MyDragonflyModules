import inspect, sys
from types import ModuleType

from dragonfly import Alternative, Repetition, CompoundRule, MappingRule, RuleRef, Grammar
from supporting import utils

# This import relies on the __all__ in __init__.py
from ccr import *


alternatives = []
# Reflect though all the members in this module to find the ones we've imported from 'ccr', and
# then instantiate those and append to alternatives to make them CCR. The nested loop here
# is awful -- must be a better way (maybe import 'ccr' directly and load the modules manually
# without even importing them (need to add each to sys.modules??): https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
for this_module_members in inspect.getmembers(sys.modules[__name__]):
    #print(mod)
    #print("loc_mem type: " + str(type(loc_mem[1])))
    if isinstance(this_module_members[1], ModuleType):
        for memb in inspect.getmembers(this_module_members[1]):
        # each member is a tuple, e.g.: ('KiloMap', <class 'ccr._continuous_rec_import.KiloMap'>)
            if inspect.isclass(memb[1]):
                #print(memb)
                clazz = memb[1]
                print("clazz: " + str(clazz))
                #print(clazz.__bases__)
                if issubclass(clazz, MappingRule) and memb[0] != "MappingRule":  # Don't try to instantiate/add MappingRule
                    print("clazz again: " + str(clazz))
                    alternatives.append(RuleRef(rule=clazz()))

# This is how to build up alternatives manually:
# alternatives = [
#     RuleRef(rule=_continuous_rec_import.TangoMap())
# ]

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
        # print "sequence: " + str(sequence)
        for action in extras["sequence"]:
            # print "action: " + str(action)
            # print "node words: " + str(node.words())
            action.execute()



chain_grammar = Grammar("chain grammar")
chain_grammar.add_rule(ChainRule())

chain_grammar.load()

def unload():
    global chain_grammar
    chain_grammar = utils.unloadHelper(chain_grammar, __name__)
