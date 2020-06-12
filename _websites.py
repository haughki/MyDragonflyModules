import webbrowser
from dragonfly import *

from supporting import utils

def openSite(site):
    webbrowser.open(site)


class WebsitesRule(MappingRule):
    mapping = {
        "web Google drive": Function(openSite, site="https://drive.google.com/drive/my-drive"),
        "web [Google] map": Function(openSite, site="maps.google.com"),
        "web Amazon [smile]": Function(openSite, site="https://smile.amazon.com"),
        "web [Google] photos": Function(openSite, site="https://photos.google.com/"),
        "web Dragon cheat sheet": Function(openSite, site="https://www.nuance.com/content/dam/nuance/en_uk/collateral/dragon/command-cheat-sheet/ct-dragon-professional-individual-en-uk.pdf"),
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