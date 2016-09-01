from dragonfly import AppContext
from dragonfly import Grammar
from dragonfly import Key, Text, Dictation, MappingRule

from languages.languages_common import specs


class PythonRule(MappingRule):
    @staticmethod
    def get_name():
        return "python"
    
    mapping = {
        "with":                         Text("with "),
        # "open file":                    Text("open('filename','r') as f:"),
        # "read lines":                   Text("content = f.readlines()"),
        # "try catch":                    Text("try:")+Key("enter:2/10, backspace")+Text("except Exception:")+Key("enter"),
        
        specs.SymbolSpecs.IF:                 Key("i,f,space,colon,left"),
        specs.SymbolSpecs.ELSE:               Text("else:")+Key("enter"),        
        specs.SymbolSpecs.BREAK:              Text("break"),

        specs.SymbolSpecs.FOR_EACH_LOOP:      Text("for in :") + Key("left:4"),
        specs.SymbolSpecs.FOR_LOOP:           Text("for i in range(0, ):")+ Key("left:2"),
        specs.SymbolSpecs.WHILE_LOOP:         Text("while :")+ Key("left"),
        
        # specs.SymbolSpecs.TO_INTEGER:         Text("int()")+ Key("left"),
        # specs.SymbolSpecs.TO_FLOAT:           Text("float()")+ Key("left"),
        # specs.SymbolSpecs.TO_STRING:          Text("str()")+ Key("left"),
        # 
        # specs.SymbolSpecs.AND:                Text(" and "),
        # specs.SymbolSpecs.OR:                 Text(" or "),
        # specs.SymbolSpecs.NOT:                Text("!"),
        # 
        # specs.SymbolSpecs.SYSOUT:             Text("print()")+Key("left"),
        # 
        # specs.SymbolSpecs.IMPORT:             Text( "import " ),
        # 
        # specs.SymbolSpecs.FUNCTION:           Text("def "),        
        # specs.SymbolSpecs.CLASS:              Text("class "),
        # 
        # specs.SymbolSpecs.COMMENT:            Text( "#" ),
        # specs.SymbolSpecs.LONG_COMMENT:       Text("''''''") + Key("left:3"),
                        
        # specs.SymbolSpecs.NULL:               Text("None"),
        # 
        # specs.SymbolSpecs.RETURN:             Text("return "),
        # 
        # specs.SymbolSpecs.TRUE:               Text("True"),
        # specs.SymbolSpecs.FALSE:              Text("False"),
                
         
        # Python specific           
         
        # "sue iffae":                    Text("if "), 
        # "sue shells":                   Text("else "),
        #   
        #  
        # "from":                         Text( "from " ),
        # "self":                         Text("self"),
        # "long not":                     Text(" not "),
        # "it are in":                    Text(" in "),          #supposed to sound like "iter in"
        # 
        # "shell iffae | LFA":            Key("e,l,i,f,space,colon,left"),
        # "convert to character":         Text("chr()")+ Key("left"),
        # "length of":                    Text("len()")+ Key("left"),
        #  
        # "global":                       Text("global "),
        #                 
        # "make assertion":               Text("assert "),
        # "list comprehension":           Text("[x for x in TOKEN if TOKEN]"),
        # 
        # "[dot] (pie | pi)":             Text(".py"),
        # "jason":                        Text("json"),
        # "identity is":                  Text(" is "),
          
         
        }

    extras   = [Dictation("text"),]
    defaults = {}
    
    token_set = specs.TokenSet(["and", "del", "from", "not", "while", "as", "elif",
                 "global", "or", "with", "assert", "else", "if", "pass",
                 "yield", "break", "except", "import", "print", "class",
                 "exec", "in", "raise", "continue", "finally", "is",
                 "return", "def", "for", "lambda", "try"], 
                         "#", 
                         ["'''", '"""'])

context = AppContext(executable="idea64") | AppContext(executable="notepad++")
python_grammar = Grammar("Python", context=context)
python_grammar.add_rule(PythonRule())
python_grammar.load()
python_grammar.disable()

def unload():
    global python_grammar
    if python_grammar:
        print "unloading " + __name__ + "..."
        python_grammar.unload()
    python_grammar = None
