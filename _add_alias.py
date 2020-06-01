from dragonfly import *
from supporting import utils

def addAlias(dictation):
    alias_name = str(dictation)
    alias_value = utils.getSelectedText()
    if not alias_value or alias_value == "":
        raise StandardError("No value for \"alias_value\".  Select some text to alias.")
    file_path = "C:\\NatLink\\NatLink\\MacroSystem\\_aliases.py"
    lines = []
    with open(file_path, 'r') as aliases:
        lines = aliases.readlines()
    with open(file_path, 'w') as aliases:
        started_mapping = False
        done_adding = False
        for line in lines:
            if done_adding:
                aliases.write(line)
                continue
            if not started_mapping:
                aliases.write(line)
                if line.find("mapping = {") != -1:
                    started_mapping = True
                    continue
            if started_mapping and not done_adding:
                if line.find("}") != -1:
                    aliases.write("        \"" + alias_name + "\": Text(\"" + alias_value + "\"),\n")
                    aliases.write(line)
                    done_adding = True
                else:
                    aliases.write(line)
    utils.toggleMicrophone()


class AddAliasRule(MappingRule):
    mapping = {
        "[add | at | had] alias <dictation>": Function(addAlias),
    }
    extras = [Dictation("dictation")]


add_alias_grammar = Grammar("add alias grammar")
add_alias_grammar.add_rule(AddAliasRule())


add_alias_grammar.load()

def unload():
    global add_alias_grammar
    add_alias_grammar = utils.unloadHelper(add_alias_grammar, __name__)