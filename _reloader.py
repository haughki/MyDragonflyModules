import os

from dragonfly import *
from reimport import reimport

from languages import python_rule, java_rule, yaml_rule, specs
from supporting import utils, character

MACROSYSTEM_DIRECTORY = "C:\\NatLinkUserDirectory"


def languageReloader():
    print "Reloading languages..."
    # Why doesn't this work?
    # modified_modules = modified(MACROSYSTEM_DIRECTORY + "\\languages")
    # for mod in modified_modules:
    #     reimport(mod)
    reimport(specs)
    reimport(python_rule, java_rule, yaml_rule)
    utils.touch(MACROSYSTEM_DIRECTORY + "\\_language_switcher.py")
    utils.toggleMicrophone()

def characterReloader():
    print "Reloading character..."
    reimport(character)
    utils.toggleMicrophone()

def utilsReloader():
    print "Reloading utils..."
    reimport(utils)
    utils.toggleMicrophone()

def reloadAll():
    print "Reloading everything in the Macrosystem directory..."
    user_directory_files = [f for f in os.listdir(MACROSYSTEM_DIRECTORY) if f.endswith('.py')]
    for the_file in user_directory_files:
        utils.touch(MACROSYSTEM_DIRECTORY + "\\" + the_file)
    utils.toggleMicrophone()

class ReloadRule(MappingRule):
    mapping = {
        "reload languages": Function(languageReloader),
        "reload character": Function(characterReloader),
        "reload utilities": Function(utilsReloader),
        "reload all [(modules | grammars)]": Function(reloadAll),
        "toggle (Mike | microphone)": Function(utils.toggleMicrophone),
    }

reload_grammar = Grammar("reloading grammar")
reload_grammar.add_rule(ReloadRule())
reload_grammar.load()

def unload():
    global reload_grammar
    if reload_grammar:
        print "unloading " + __name__ + "..."
        reload_grammar.unload()
    reload_grammar = None
