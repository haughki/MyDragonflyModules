import webbrowser

from dragonfly import *

def openSite(site):
    webbrowser.open(site)


class Example(MappingRule):
    mapping = {
        "web Google drive": Function(openSite, site="https://drive.google.com/drive/my-drive"),
        "web [Google] map": Function(openSite, site="maps.google.com"),
        "web Amazon [smile]": Function(openSite, site="https://smile.amazon.com")
    }
    extras = [Dictation("text"),
              ]
    defaults = {"text":None}


example_grammar = Grammar("example grammar")
example_grammar.add_rule(Example())


example_grammar.load()

def unload():
    global example_grammar
    if example_grammar:
        print "unloading " + __name__ + "..."
        example_grammar.unload()
    example_grammar = None
