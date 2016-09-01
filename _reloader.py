
# import sys
# sys.path.append('pycharm-debug.egg')
# import pydevd
# pydevd.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)

from dragonfly import *
from natlinkmain import micOnCallback, natDisconnect, start_natlink

from supporting import utils
from reimport import reimport
#reimport(_python_rule)
#reimport(specs)

MACROSYSTEM_DIRECTORY = "C:\\NatLink\\NatLink\\MacroSystem"

def restartNatlink():
    print "Restarting NatLink d..."
    natDisconnect()
    start_natlink(True)

def languageReloader():
    print "Reloading languages..."
    # pp = pprint.PrettyPrinter()
    # pp.pprint(sys.modules)
    # languages._python_rule.pythonRuleReimport()
    micOnCallback()
    utils.touch(MACROSYSTEM_DIRECTORY + "\\languages\\_python_rule.py")
    micOnCallback()
    utils.touch(MACROSYSTEM_DIRECTORY + "\\_multiedit.py")
    micOnCallback()

class ReloadRule(MappingRule):
    mapping = {
        "reload languages": Function(languageReloader),
        "restart (natlink | NatLink | Natlink)": Function(restartNatlink),
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
