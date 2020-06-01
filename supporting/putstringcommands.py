from dragonfly.actions.action_text import Text
from dragonfly.grammar.rule_mapping import MappingRule

__author__ = 'parkerh'


class PutStringCommandsRule(MappingRule):
    mapping = {
        "put e-mail": Text("parker.hawkeye@gmail.com"),
        "put first": Text("Hawkeye"),
        "put last": Text("Parker"),
        "put [whole] name": Text("Hawkeye Parker"),
        "put address": Text("56 Elizabeth Way"),
        "put city": Text("San Rafael"),
        "put state": Text("CA"),
        "put zip": Text("94901"),
        "put phone": Text("415 297 6170"),
        "put Google phone": Text("415 548 1460"),
        "put user": Text("haughki"),
        }
