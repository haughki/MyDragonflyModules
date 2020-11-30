# import pydevd_pycharm
# pydevd_pycharm.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)


from dragonfly import *
from supporting import utils

class Example2(Rule):
    def __init__(
            self, name=None, element=None, context=None, imported=False, exported=True
    ):
        Rule.__init__(
            self,
            name=name,
            element=element,
            context=context,
            imported=imported,
            exported=exported,
        )

    def process_recognition(self, node):
        print "hutch"



# class Example2(MappingRule):
#
#     def __init__(self, name=None, mapping=None, extras=None, defaults=None, exported=False, context=None):
#         MappingRule.__init__(self, name=name, mapping=mapping, extras=extras, defaults=defaults, exported=exported, context=context)
#
#     def value(self, node):
#         node = node.children[0]
#         value = node.value()
#
#         if hasattr(value, "copy_bind"):
#             # Prepare *extras* dict for passing to _copy_bind().
#             extras = {
#                 "_grammar":  self.grammar,
#                 "_rule":     self,
#                 "_node":     node,
#             }
#             extras.update(self._defaults)
#             for name, element in self._extras.items():
#                 extra_node = node.get_child_by_name(name, shallow=True)
#                 if extra_node:
#                     extras[name] = extra_node.value()
#                 elif element.has_default():
#                     extras[name] = element.default
#
#             value = value.copy_bind(extras)
#
#         return value






example2_grammar = Grammar("example2 grammar")
example2_grammar.add_rule(Example2(name="bitchin car",
                                   element=Alternative([Literal("friend"), Literal("foe")])
                                   ))
example2_grammar.load()

def unload():
    global example2_grammar
    example2_grammar = utils.unloadHelper(example2_grammar, __name__)