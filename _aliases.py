from dragonfly import MappingRule, Text, Grammar
from supporting import utils



class Aliases(MappingRule):
    mapping = {
        "Rumpelstiltskin": Text("placeholder alias"),
    }

aliases_grammar = Grammar("The actual aliases grammar")
aliases_grammar.add_rule(Aliases())


aliases_grammar.load()

def unload():
    global aliases_grammar
    aliases_grammar = utils.unloadHelper(aliases_grammar, __name__)
    
