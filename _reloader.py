import os

from dragonfly import *
from reimport import reimport

from languages import python_rule, java_rule, yaml_rule, specs
from supporting import utils, character
#from ccr import _continuous_rec_import

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

# reloading for CCR is going to be really complicated. Punt for now.
# def ccrReloader():
#     print "Reloading CCR..."
#     reimport(_continuous_rec_import)
#     utils.touch(MACROSYSTEM_DIRECTORY + "\\_continuous_recognition_skeleton.py")
#     utils.toggleMicrophone()

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
#        "reload continuous": Function(ccrReloader),
        "reload all [(modules | grammars)]": Function(reloadAll),
    }

reload_grammar = Grammar("reloading grammar")
reload_grammar.add_rule(ReloadRule())
reload_grammar.load()

def unload():
    global reload_grammar
    reload_grammar = utils.unloadHelper(reload_grammar, __name__)