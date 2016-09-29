# import sys
# sys.path.append('pycharm-debug.egg')
# import pydevd
# pydevd.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)
from dragonfly import Dictation
from dragonfly import Key, Text, MappingRule

from languages import specs


class PythonRule(MappingRule):
    mapping = {
            "(shells | else) if":                   Key("e,l,i,f,space,colon,left"),
            specs.SymbolSpecs.IF:                   Key("i,f,space,colon,left"),
            specs.SymbolSpecs.ELSE:                 Text("else:") + Key("enter"),
            specs.SymbolSpecs.DEFINE_METHOD:        Text("def ():") + Key("left:3"),
            "define self":                          Text("def (self):") + Key("left:7"),
            specs.SymbolSpecs.FOR_LOOP:             Text("for i in range(0, ):") + Key("left:2"),
            specs.SymbolSpecs.FOR_EACH_LOOP:        Text("for in :") + Key("left:4"),
            specs.SymbolSpecs.SYSOUT:               Text("print "),
            specs.SymbolSpecs.TO_STRING:            Text("str()") + Key("left"),

            "with":                         Text("with "),
            # "open file":                    Text("open('filename','r') as f:"),
            # "read lines":                   Text("content = f.readlines()"),
            # "try catch":                    Text("try:")+Key("enter:2/10, backspace")+Text("except Exception:")+Key("enter"),
    
            specs.SymbolSpecs.BREAK:              Text("break"),    
            specs.SymbolSpecs.WHILE_LOOP:         Text("while :")+ Key("left"),
    
            specs.SymbolSpecs.TO_INTEGER:         Text("int()")+ Key("left"),
            specs.SymbolSpecs.TO_FLOAT:           Text("float()")+ Key("left"),
    
            specs.SymbolSpecs.AND:                Text(" and "),
            specs.SymbolSpecs.OR:                 Text(" or "),
            specs.SymbolSpecs.NOT:                Text("!"),
            
            specs.SymbolSpecs.IMPORT:             Text( "import " ),    
            specs.SymbolSpecs.CLASS:              Text("class ") + Text("%(text)s:") + Key("enter"),
            specs.SymbolSpecs.COMMENT:            Text( "#" ),
            specs.SymbolSpecs.LONG_COMMENT:       Text("\"\"\""),
            specs.SymbolSpecs.NOT_EQUAL_NULL:     Text(" not None"),
            specs.SymbolSpecs.NULL:               Text("None"),
            specs.SymbolSpecs.RETURN:             Text("return "),
            specs.SymbolSpecs.TRUE:               Text("True"),
            specs.SymbolSpecs.FALSE:              Text("False"),
        
            # "sue iffae":                    Text("if "), 
            # "sue shells":                   Text("else "),
        
            "from":                         Text( "from " ),
            "self":                         Text("self"),
            "long not":                     Text(" not "),
            "it are in":                    Text(" in "),          #supposed to sound like "iter in"
            # "shell iffae | LFA":            Key("e,l,i,f,space,colon,left"),
            "convert to character":         Text("chr()")+ Key("left"),
            "global":                       Text("global "),
            "list comprehension":           Text("[x for x in if ]"),
            "[dot] (pie | pi)":             Text(".py"),
            "identity is":                  Text(" is "),
            "length ":                      Text("len()") + Key("left"),
            
    }            
    extras = [
        Dictation("modifiers"),
        Dictation("text"),
    ]
    defaults = {
        "modifiers": None,
    }
