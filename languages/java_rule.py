import sys
sys.path.append('pycharm-debug.egg')
import pydevd
pydevd.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)

from dragonfly import Key, Text, MappingRule

class JavaRule(MappingRule):

    mapping = {
        "deco override":                    Text("@Override"),
        "if then":                     Text("if() {")+Key("enter,up,left"),
    }

