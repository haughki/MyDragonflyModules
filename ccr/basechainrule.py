# import pydevd_pycharm
# pydevd_pycharm.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)

from dragonfly import Alternative, Repetition, CompoundRule


class BaseChainRule(CompoundRule):
    def __init__(self, alternatives, name=None, defaults=None, exported=None, context=None):
        CompoundRule.__init__(self, name=name, spec="<sequence>",
                              extras=[Repetition(Alternative(alternatives), min=1, max=16, name="sequence")],
                              defaults=defaults, exported=exported, context=context)

    #  - node -- root node of the recognition parse tree.
    #  - extras -- dict of the "extras" special elements:
    #     . extras["sequence"] gives the sequence of actions.
    def _process_recognition(self, node, extras):
        # print "extras: " + str(extras)
        # print "sequence: " + str(sequence)
        # print "node words: " + str(node.words())
        # print "node: " + str(node)

        for action in extras["sequence"]:
            # print "action: " + str(action)
            action.execute()



