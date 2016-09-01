from dragonfly import AppContext
from dragonfly import Grammar
from dragonfly import Key, Text, Dictation, MappingRule

from languages.languages_common import specs


class JavaRule(MappingRule):

    @staticmethod
    def get_name():
        return "java"

    mapping = {
        # "try catch":                        Text("try{}catch(Exception e){}"),
        "deco override":                    Text("@Override"),
        # # "iterate and remove":               Paste("for (Iterator<TOKEN> iterator = TOKEN.iterator(); iterator.hasNext();) {\n\tString string = iterator.next();\nif (CONDITION) {\niterator.remove();\n}\n}"),
        # # "string builder":                   Paste("StringBuilder builder = new StringBuilder(); builder.append(orgStr); builder.deleteCharAt(orgStr.length()-1);"),
        # 
        specs.SymbolSpecs.IF:                     Text("if() {")+Key("enter,up,left"),
        # specs.SymbolSpecs.ELSE:                   Text("else {")+Key("enter"),
        # #
        # specs.SymbolSpecs.SWITCH:                 Text("switch(){\ncase : break;\ndefault: break;")+Key("up,up,left,left"),
        # specs.SymbolSpecs.CASE:                   Text("case :")+Key("left"),
        # specs.SymbolSpecs.BREAK:                  Text("break;"),
        # specs.SymbolSpecs.DEFAULT:                Text("default: "),
        # #
        # specs.SymbolSpecs.DO_LOOP:                Text("do {}")+Key("left, enter:2"),
        # specs.SymbolSpecs.WHILE_LOOP:             Text("while ()")+Key("left"),
        # specs.SymbolSpecs.FOR_LOOP:               Text("for (int i=0; i<TOKEN; i++)"),
        # specs.SymbolSpecs.FOR_EACH_LOOP:          Text("for (TOKEN TOKEN : TOKEN)"),
        # #
        # # specs.SymbolSpecs.TO_INTEGER:             Text("Integer.parseInt()")+ Key("left"),
        # # specs.SymbolSpecs.TO_FLOAT:               Text("Double.parseDouble()")+ Key("left"),
        # # specs.SymbolSpecs.TO_STRING:              Key("dquote, dquote, plus"),
        # # #
        # # specs.SymbolSpecs.AND:                    Text(" && "),
        # # specs.SymbolSpecs.OR:                     Text(" || "),
        # # specs.SymbolSpecs.NOT:                    Text("!"),
        # # #
        # # specs.SymbolSpecs.SYSOUT:                 Text("java.lang.System.out.println()")+Key("left"),
        # # #
        # # specs.SymbolSpecs.IMPORT:                 Text( "import " ),
        # # #
        # # specs.SymbolSpecs.FUNCTION:               Text("TOKEN(){}")+Key("left"),
        # # specs.SymbolSpecs.CLASS:                  Text("class {}")+Key("left/5:2"),
        # # #
        # # specs.SymbolSpecs.COMMENT:                Text( "//" ),
        # # specs.SymbolSpecs.LONG_COMMENT:           Text("/**/")+Key("left,left"),
        # # #
        # # specs.SymbolSpecs.NULL:                   Text("null"),
        # # #
        # # specs.SymbolSpecs.RETURN:                 Text("return "),
        # # #
        # # specs.SymbolSpecs.TRUE:                   Text("true"),
        # # specs.SymbolSpecs.FALSE:                  Text("false"),
        # # 
        # # 
        # # # Java specific
        # # 
        # # "it are in":                        Text("Arrays.asList(TOKEN).contains(TOKEN)"),
        # # "try states":                       Text("try"),
        # # "arrow":                            Text("->"),
        # # 
        # # "public":                           Text("public "),
        # # "private":                          Text("private "),
        # # "static":                           Text("static "),
        # # "final":                            Text("final "),
        # # "void":                             Text("void "),
        # # 
        # # "cast to double":                   Text("(double)()")+Key("left"),
        # # "cast to integer":                  Text("(int)()")+Key("left"),
        # #         
        # # "new new":                          Text("new "),
        # # "integer":                          Text("int "),
        # # "big integer":                      Text("Integer "),
        # # "double tie":                       Text("double "),
        # # "big double":                       Text("Double "),
        # # 
        # # "string":                           Text("String "),
        # # "boolean":                          Text("boolean "),
        # # "substring":                        Text("substring"),
        # #  
        # # "ternary":                          Text("()?:") + Key("left:3"),
        # # "this":                             Text("this"),
        # # "array list":                       Text("ArrayList"),
        # # 
        # # "continue":                         Text("continue"),
        # # "sue iffae":                        Text("if ()")+Key("left"),
        # # "sue shells":                       Text("else")+Key("enter"),
        # # 
        # # "shell iffae":                      Text("else if ()")+Key("left"),
        # # "throw exception":                  Text("throw new Exception()")+Key("left"),
        # # 
        # # "character at":                     Text("charAt"),
        # # "is instance of":                   Text(" instanceof "),
          
    }

    extras   = []
    defaults = {}
    
    token_set = specs.TokenSet(["abstract", "continue", "for", "new", "switch", "assert",
                 "default", "goto", "package", "synchronized", "boolean",
                 "do", "if", "private", "this", "break", "double",
                 "implements", "protected", "throw", "byte", "else",
                 "import", "public", "throws", "case", "enum",
                 "instanceof", "return", "transient", "catch", "extends",
                 "int", "short", "try", "char", "final", "interface",
                 "static", "void", "class", "finally", "long", "strictfp",
                 "volatile", "const", "float", "native", "super", "while"], 
                         "//", 
                         ["/*", "*/"])


context = AppContext(executable="idea64") | AppContext(executable="notepad++")
java_grammar = Grammar("Java", context=context)
java_grammar.add_rule(JavaRule())
java_grammar.load()
java_grammar.disable()

def unload():
    global java_grammar
    if java_grammar:
        print "unloading " + __name__ + "..."
        java_grammar.unload()
    java_grammar = None