
# import sys
# sys.path.append('pycharm-debug.egg')
# import pydevd
# pydevd.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)

from dragonfly import *
#from natlinkmain import micOnCallback, natDisconnect, start_natlink

from supporting import utils
from reimport import reimport
from languages import python_rule


MACROSYSTEM_DIRECTORY = "C:\\NatLink\\NatLink\\MacroSystem"

def restartNatlink():
    print "Restarting NatLink d..."
    # natDisconnect()
    # start_natlink(True)

def languageReloader():
    print "Reloading languages..."

    # manually reload python_rule
    reimport(python_rule)
    
    # touch switcher
    utils.touch(MACROSYSTEM_DIRECTORY + "\\_switcher.py")
    
    # toggle mic
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
