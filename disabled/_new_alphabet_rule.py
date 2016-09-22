from dragonfly import Alternative
from dragonfly import CompoundRule
from dragonfly import Grammar
from dragonfly import IntegerRef
from dragonfly import Key
from dragonfly import MappingRule
from dragonfly import Repetition
from dragonfly import RuleRef


class NewAlphabetRule(MappingRule):
    exported = False
    mapping = {
        "Alpha [<n>]": Key("a:%(n)d"),
        "Bravo [<n>]": Key("b:%(n)d"),
        "Charlie [<n>]": Key("c:%(n)d"),
        "Delta [<n>]": Key("d:%(n)d"),
        "Echo [<n>]": Key("e:%(n)d"),
        "Foxtrot [<n>]": Key("f:%(n)d"),
        "Golf [<n>]": Key("g:%(n)d"),
        "Hotel [<n>]": Key("h:%(n)d"),
        "Ice [<n>]": Key("i:%(n)d"),
        "Juneau [<n>]": Key("j:%(n)d"),
        "Kilo [<n>]": Key("k:%(n)d"),
        "Lima [<n>]": Key("l:%(n)d"),
        "Monty [<n>]": Key("m:%(n)d"),
        "Ninja [<n>]": Key("n:%(n)d"),
        "Oscar [<n>]": Key("o:%(n)d"),
        "Papa [<n>]": Key("p:%(n)d"),
        "Quinn [<n>]": Key("q:%(n)d"),
        "Robin [<n>]": Key("r:%(n)d"),
        "Soda [<n>]": Key("s:%(n)d"),
        "Tango [<n>]": Key("t:%(n)d"),
        "Usurp [<n>]": Key("u:%(n)d"),
        "Victor [<n>]": Key("v:%(n)d"),
        "Whiskey [<n>]": Key("w:%(n)d"),
        "X-ray [<n>]": Key("x:%(n)d"),
        "Yankee [<n>]": Key("y:%(n)d"),
        "Zulu [<n>]": Key("z:%(n)d"),
    }
    extras = [IntegerRef("n", 1, 100),]
    defaults = {"n": 1,}


alternatives = []
alternatives.append(RuleRef(rule=NewAlphabetRule()))

single_action = Alternative(alternatives)

sequence = Repetition(single_action, min=1, max=16, name="sequence")


class AlphabetChainRule(CompoundRule):
    spec = "<sequence>"
    extras = [
        sequence, # Sequence of actions defined above.
    ]

    #  - node -- root node of the recognition parse tree.
    #  - extras -- dict of the "extras" special elements:
    #     . extras["sequence"] gives the sequence of actions.
    def _process_recognition(self, node, extras):
        sequence = extras["sequence"]   # A sequence of actions.
        # print "sequence: " + str(sequence)
        for action in sequence:
            # print "action: " + str(action)
            # print "node words: " + str(node.words())
            action.execute()


new_alphabet_grammar = Grammar("New Alphabet")   # Create this module's grammar.
new_alphabet_grammar.add_rule(AlphabetChainRule())    # Add the top-level rule.
new_alphabet_grammar.load()                    # Load the grammar.

def unload():
    global new_alphabet_grammar
    if new_alphabet_grammar:
        print "unloading " + __name__ + "..."
        new_alphabet_grammar.unload()
    new_alphabet_grammar = None