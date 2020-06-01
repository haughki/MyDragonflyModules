import webbrowser
from dragonfly import *

from supporting import utils

def openSite(site):
    webbrowser.open(site)


class WebsitesRule(MappingRule):
    mapping = {
        "web Google drive": Function(openSite, site="https://drive.google.com/drive/my-drive"),
        "web [Google] map": Function(openSite, site="maps.google.com"),
        "web Amazon [smile]": Function(openSite, site="https://smile.amazon.com")
    }
    extras = [Dictation("text"),
              ]
    defaults = {"text":None}


websites_grammar = Grammar("Open certain websites")
websites_grammar.add_rule(WebsitesRule())


websites_grammar.load()

def unload():
    global websites_grammar
    websites_grammar = utils.unloadHelper(websites_grammar, __name__)