# import sys
# sys.path.append('pycharm-debug.egg')
# import pydevd
# pydevd.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)

from dragonfly import *
from reimport import reimport, modified

from languages import python_rule, java_rule, specs
from supporting import utils

MACROSYSTEM_DIRECTORY = "C:\\NatLink\\NatLink\\MacroSystem"

def languageReloader():
    print "Reloading languages..."
    # Why doesn't this work?
    # modified_modules = modified(MACROSYSTEM_DIRECTORY + "\\languages")
    # for mod in modified_modules:
    #     reimport(mod)
    reimport(specs)
    reimport(python_rule, java_rule)
    utils.touch(MACROSYSTEM_DIRECTORY + "\\_language_switcher.py")
    Key("npadd/10,npadd").execute()


class ReloadRule(MappingRule):
    mapping = {
        "reload languages": Function(languageReloader),
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
