from dragonfly import Dictation
from dragonfly import Key, Text, MappingRule

from languages import specs


class YamlRule(MappingRule):
    mapping = {
            specs.SymbolSpecs.SYSOUT:               Text("- debug: \n\t\tmsg: "),

            specs.SymbolSpecs.TO_INTEGER:         Text("|int "),
            specs.SymbolSpecs.TO_FLOAT:           Text("|float"),
            specs.SymbolSpecs.TO_STRING:           Text("|str"),
            specs.SymbolSpecs.GET_LENGTH:           Text("|length"),

            specs.SymbolSpecs.AND:                Text(" and "),
            specs.SymbolSpecs.OR:                 Text(" or "),
            specs.SymbolSpecs.NOT:                Text(" not "),

            specs.SymbolSpecs.IMPORT:             Text("import_tasks"),
            specs.SymbolSpecs.NOT_EQUAL_NULL:     Text(" is not undefined"),
            specs.SymbolSpecs.NULL:               Text(" is undefined"),
            specs.SymbolSpecs.TRUE:               Text("True"),
            specs.SymbolSpecs.FALSE:              Text("False"),

            "(started | start it)": Text("- "),
            "start when": Text("- when: "),
            "long not":                     Text(" not "),
            "it are in":                    Text(" in "),          #supposed to sound like "iter in"
            # "convert to int":               Text("|int "),
            "[dot] (pie | pi)":             Text(".py"),
            "dot YAML":                     Text(".yml"),
            "(create | define) variable": Text("- set_fact:\n\t\t"),
            "(print | debug) variable": Text("- debug: var="),
            "(print | debug) message": Text("- debug:\n\t\tmsg: "),
            "(extract | get) variable": Text("\"{{}}\"") + Key("left:3")
    }
    extras = [
        Dictation("modifiers"),
        Dictation("text"),
    ]
    defaults = {
        "modifiers": None,
    }
