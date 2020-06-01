# import pydevd_pycharm
# pydevd_pycharm.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)


from dragonfly import CompoundRule, MappingRule, Grammar
from dragonfly import get_engine
from supporting import utils

def _print_rule(grammar, rule):
    if rule.exported:
        _print_rule_details("", grammar, rule)
    else:
        # print "\t-------- NOT EXPORTED ---------"
        _print_rule_details("\t-------- NOT EXPORTED ---------", grammar, rule)

def _print_rule_details(msg, grammar, rule):

    if isinstance(rule, MappingRule):
        for sp in rule.specs:
            #print "\t\t" + str(sp)
            pass
    elif isinstance(rule, CompoundRule):
        print grammar
        if msg:
            print msg
        print "\t" + str(rule)
        print "\t\t" + str(rule.spec)
    else:
        if msg:
            print msg
        print "\t" + str(rule)
        print "\t------------------> UNKNOWN RULE TYPE"



class ListAllCommandsRule(CompoundRule):
    spec = "list [all] commands"  # Spoken form of command.

    def _process_recognition(self, node, extras):  # Callback when command is spoken.
        engine = get_engine()
        grammars = engine.grammars

        for grammar in grammars:
            # print "{:7} : {:75} : {}".format(window.handle, window.executable.encode("utf-8"), window.title.encode("utf-8"))

            # if str(grammar) == "Grammar(VsCode)":
            #print grammar
            for rule in grammar.rules:
                _print_rule(grammar, rule)




list_commands_grammar = Grammar("List all dragonfly commands.")
list_commands_grammar.add_rule(ListAllCommandsRule())

list_commands_grammar.load()


def unload():
    global list_commands_grammar
    list_commands_grammar = utils.unloadHelper(list_commands_grammar, __name__)