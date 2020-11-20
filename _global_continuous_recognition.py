# import pydevd_pycharm
# pydevd_pycharm.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)

from dragonfly import Alternative, Repetition, CompoundRule, RuleRef, Grammar
from supporting import utils

from ccr import editing_commands, text_formatting, scan_line, window_control


alternatives = [
    RuleRef(rule=editing_commands.MultiEditRule()),
    RuleRef(rule=text_formatting.FormatRule()),
    RuleRef(rule=scan_line.ScanLineRule()),
    RuleRef(rule=window_control.PlaceFractionRule()),
    RuleRef(rule=window_control.FocusWinRule()),
    RuleRef(rule=window_control.FocusTitleRule()),
    RuleRef(rule=window_control.TranslateRule()),
    RuleRef(rule=window_control.NudgeRule()),
    RuleRef(rule=window_control.ResizeRule()),
    RuleRef(rule=window_control.StretchRule()),
]

try:  # putstringcommands is not included in the pushed source, because it contains personal data.
    from ccr import putstringcommands

    if putstringcommands.PutStringCommandsRule:
        alternatives.append(RuleRef(rule=putstringcommands.PutStringCommandsRule()))
except (ImportError, NameError) as e:
    pass

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
        # print "extras: " + str(extras)
        # print "sequence: " + str(sequence)
        # print "node words: " + str(node.words())
        # print "node: " + str(node)

        for action in extras["sequence"]:
            # print "action: " + str(action)
            action.execute()



chain_grammar = Grammar("chain grammar")
chain_grammar.add_rule(ChainRule())

chain_grammar.load()

def unload():
    global chain_grammar
    chain_grammar = utils.unloadHelper(chain_grammar, __name__)
