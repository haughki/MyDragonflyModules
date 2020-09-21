from dragonfly import CompoundRule, Function
from dragonfly.actions.action_base import BoundAction

""" Rule to support adding a CompoundRule to the 'global continuous recognition system'.
    This rule overrides value() to produce a BoundAction, very similar to the way
    MappingRules work (see MappingRule.value()). In this way, the CCR rule can execute
    the _process_recognition() method as an Action, the same way it does for items in
    a MappingRule.
    """
class CCRCompoundRule(CompoundRule):

    def __init__(self, name=None, spec=None, extras=None, defaults=None, exported=None, context=None):

        CompoundRule.__init__(self, name=name, spec=spec, extras=extras, defaults=defaults, exported=exported, context=context)

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