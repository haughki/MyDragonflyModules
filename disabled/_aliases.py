from dragonfly import MappingRule, Text, Grammar


class Aliases(MappingRule):
    mapping = {
        "short object": Text("obj"),
        "short string": Text("str"),
    }

example_grammar = Grammar("alias grammar")
example_grammar.add_rule(Aliases())


example_grammar.load()

def unload():
    global example_grammar
    if example_grammar:
        print "unloading " + __name__ + "..."
        example_grammar.unload()
    example_grammar = None
