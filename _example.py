from dragonfly import *
from supporting import utils

def snake_text(snaketext=""):
    snaked = snaketext.lower().replace(" ", "_")
    Text("def " + snaked +"():").execute()
    Key("left:2").execute()


class Example(MappingRule):
    context = AppContext(executable="code")  # app-specific context
    #exported = False
    mapping = {
        "command one": Text("comm 1   "),
        "command two": Text("comm 2   "),
        "function [<snaketext>]": Function(snake_text) ,

    }

    extras = [
        Dictation("snaketext", default=""),
        Dictation("classtext", default="").title().replace(" ", ""),
    ]


example_grammar = Grammar("example grammar")
example_grammar.add_rule(Example())
example_grammar.load()

def unload():
    global example_grammar
    example_grammar = utils.unloadHelper(example_grammar, __name__)