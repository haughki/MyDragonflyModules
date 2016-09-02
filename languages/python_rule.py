import sys
sys.path.append('pycharm-debug.egg')
import pydevd
pydevd.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)

from dragonfly import Key, Text, MappingRule

class PythonRule(MappingRule):
    mapping = {
            "with sugar":                         Text("is tasty"),
            "pushing through":                         Text("the market square"),
            "so many mothers":                         Text("sighing"),
            "if then":                 Key("i,f,space,colon,left"),         
        }


