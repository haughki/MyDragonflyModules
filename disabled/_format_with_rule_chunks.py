from dragonfly import *
from dragonfly.actions.action_base import BoundAction


"""
Extends the formatting functions of multiedit, by allowing you to, alternatively, call out a mapping rule command
to join with the dictation.  Intention is to allow you to say something like:

"score next object"

where "object" is regular dictation, but "next" is a command which maps to Text("nxt"); the final result would be
"nxtObject".
"""
def format_score_function(repeated_choices):
    print repeated_choices
    words = []
    for choice in repeated_choices:
        if isinstance(choice, BoundAction):
            words.append(choice._action._spec)
        else:
            words.append(str(choice))
    print words
    print "_".join(words)


class DirkRule(MappingRule):
    mapping = {
        "Dirk": Text("smirk"),
    }


alternatives = [Dictation("dictation"), RuleRef(rule=DirkRule())]
either_one = Alternative(alternatives)
repeated_choices = Repetition(either_one, min=1, max=6, name="repeated_choices")

class Example(MappingRule):
    mapping = {
        "chore <repeated_choices>": Function(format_score_function)
    }

    extras = [repeated_choices,]

example_grammar = Grammar("example grammar")
example_grammar.add_rule(Example())


example_grammar.load()

def unload():
    global example_grammar
    if example_grammar:
        print "unloading " + __name__ + "..."
        example_grammar.unload()
    example_grammar = None
