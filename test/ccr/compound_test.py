from dragonfly import CompoundRule, Integer, Dictation, Function
from dragonfly.actions.action_base import BoundAction

""" Test rule for adding a CompoundRule to the 'global continuous recognition system'.
    This rule overrides value() to produce a BoundAction, very similar to the way
    MappingRules work (see MappingRule.value()). In this way, the CCR rule can execute
    the _process_recognition() method as an Action, the same way it does for items in
    a MappingRule.
    """
class CompoundTestCCR(CompoundRule):
    spec = "compound testing <text>"
    extras = [
        Integer("t", 1, 50),
        Dictation("text"),
    ]
    defaults = {
        "t": 1,
    }

    def _process_recognition(self, node, extras):
        print "testing the compound: " + extras["text"]


    def value(self, node):
        extras = {
            "_grammar":  self.grammar,
            "_rule":     self,
            "_node":     node,
        }
        extras.update(self.defaults)
        for name, element in self._extras.items():
            extra_node = node.get_child_by_name(name, shallow=True)
            if extra_node:
                extras[name] = extra_node.value()
            elif element.has_default():
                extras[name] = element.default
            #extras[name] = element.value()

        return BoundAction(Function(self._process_recognition), {"node": node, "extras": extras})