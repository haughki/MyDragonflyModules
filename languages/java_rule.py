# import sys
# sys.path.append('pycharm-debug.egg')
# import pydevd
# pydevd.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)


from dragonfly import Dictation
from dragonfly import Function
from dragonfly import Key, Text, MappingRule

from languages import specs
from supporting import utils


def defineGeneric(text, generic_type):
    formatted_text = ""
    if text:
        format_me = str(text)
        formatted_text = utils.text_to_case("pascal", format_me)
    Text(generic_type + formatted_text + "> ").execute()
    

def defineArrayList(text):
    defineGeneric(text, "ArrayList<")


def defineHashMap(text):
    defineGeneric(text, "HashMap<")

    
def getModifiers(words):
    modifiers_string = ""
    if len(words) > 0:
        modifiers = words
        for modifier in modifiers:
            modifiers_string = modifiers_string + modifier + " "
    return modifiers_string


def printModifiers(_node):
    Text(getModifiers(_node.words())).execute()

    
def defineMethod(text, _node):
    commands = _node.words()
    method_index = commands.index("method")
    modifiers_string = getModifiers(commands[:method_index])
    formatted_class_name = ""
    if text:
        format_me = str(text)
        if len(commands) > method_index + 1:
            format_command = commands[method_index + 1]
            if (format_command != "pascal") and (format_command !="snake"):
                format_command = "camel"  # default
            formatted_class_name = utils.text_to_case(format_command, format_me)
    (Text(modifiers_string + formatted_class_name + "() {") + Key("enter, up, end, left:3")).execute()    
    
        
def defineClass(text, _node):
    commands = _node.words()
    class_index = commands.index("class")
    modifiers_string = getModifiers(commands[:class_index])
    formatted_class_name = ""
    if text:
        format_me = str(text)
        if len(commands) > class_index + 1:
            format_command = commands[class_index + 1]
            if (format_command != "camel") and (format_command !="snake"):
                format_command = "pascal"  # default
            formatted_class_name = utils.text_to_case(format_command, format_me)
    (Text(modifiers_string + "class " + formatted_class_name + " {") + Key("enter")).execute()


class JavaRule(MappingRule):
    INTELLIJ_POPUP_DELAY = "10"    
    mapping = {
        specs.SymbolSpecs.IF:                       Text("if(){") + Key("enter,up,left"),
        # specs.SymbolSpecs.IF:                       Key("dot, i, f/" + INTELLIJ_POPUP_DELAY + ", enter"),
        specs.SymbolSpecs.ELSE:                     Text("else {") + Key("enter"),
        specs.SymbolSpecs.DEFINE_METHOD:            Function(defineMethod),
        # specs.SymbolSpecs.SWITCH:                   Text("switch(){\ncase : break;\ndefault: break;")+Key("up,up,left,left"),
        specs.SymbolSpecs.SWITCH:                   Key("dot, s, w, i, t, c, h/" + INTELLIJ_POPUP_DELAY + ", enter"),                   
        specs.SymbolSpecs.CASE:                     Text("case :")+Key("left"),
        specs.SymbolSpecs.BREAK:                    Text("break;"),
        specs.SymbolSpecs.DEFAULT:                  Text("default: "),
        specs.SymbolSpecs.DO_LOOP:                  Text("do {}")+Key("left, enter:2"),
        # specs.SymbolSpecs.WHILE_LOOP:               Text("while ()")+Key("left"),
        specs.SymbolSpecs.WHILE_LOOP:               Key("dot, w, h, i, l, e/" + INTELLIJ_POPUP_DELAY + ", enter"),               
        # specs.SymbolSpecs.FOR_LOOP:                 Text("for (int i=0; i< ; i++){") + Key("enter,up"),
        specs.SymbolSpecs.FOR_LOOP:                 Key("dot, f, o, r, i/" + INTELLIJ_POPUP_DELAY + ", enter"),
        # specs.SymbolSpecs.FOR_EACH_LOOP:            Text("for( : ){") + Key("enter,up"),
        specs.SymbolSpecs.FOR_EACH_LOOP:            Key("dot, f, o, r/" + INTELLIJ_POPUP_DELAY + ", enter"),
        specs.SymbolSpecs.TRY_CATCH:                Key("dot, t, r, y/" + INTELLIJ_POPUP_DELAY + ", enter"),
        
        specs.SymbolSpecs.TO_INTEGER:               Text("Integer.parseInt()")+ Key("left"),
        specs.SymbolSpecs.TO_STRING:                Text(".toString()"),
        
        specs.SymbolSpecs.AND:                      Text(" && "),
        specs.SymbolSpecs.OR:                       Text(" || "),
        specs.SymbolSpecs.NOT:                      Text("!"),
        
        # specs.SymbolSpecs.SYSOUT:                   Text("System.out.println()")+Key("left"),
        specs.SymbolSpecs.SYSOUT:                   Key("dot, s, o, u, t/" + INTELLIJ_POPUP_DELAY + ", enter"),
        specs.SymbolSpecs.IMPORT:                   Text( "import " ),
        specs.SymbolSpecs.FUNCTION:                 Text("(){")+Key("left"),
        specs.SymbolSpecs.CLASS:                    Function(defineClass),

        specs.SymbolSpecs.COMMENT:                  Text( "// " ),
        specs.SymbolSpecs.LONG_COMMENT:             Text("/**/")+Key("left,left"),
        specs.SymbolSpecs.NULL:                     Text("null"),
        specs.SymbolSpecs.NOT_EQUAL_NULL:           Key("dot, n, u, l, l/" + INTELLIJ_POPUP_DELAY + ", enter"),
        specs.SymbolSpecs.RETURN:                   Key("dot, r, e, t, u, r, n/" + INTELLIJ_POPUP_DELAY + ", enter"),
        specs.SymbolSpecs.TRUE:                     Text("true"),
        specs.SymbolSpecs.FALSE:                    Text("false"),
        
        # "it are in": Text("Arrays.asList(TOKEN).contains(TOKEN)"),
        "[(public | protected | private)] [static] [final]": Function(printModifiers),
        "is not null": Key("dot, n, o, t, n, u, l, l/" + INTELLIJ_POPUP_DELAY + ", enter"),
        "create field": Key("dot, f, i, e, l, d/" + INTELLIJ_POPUP_DELAY + ", enter"),
        "try with resources": Key("dot, t, w, r/"  + INTELLIJ_POPUP_DELAY + ", enter"),
        "array to stream": Key("dot, s, t, r, e, a, m/" + INTELLIJ_POPUP_DELAY + ", enter"),
        "deco override": Text("@Override"),
        "generic list": Text("List<>") + Key("left"),
        "generic map": Text("Map<>") + Key("left"),
        "convert (array | hooray) to list": Text("Arrays.asList("),
        "new in line list": Text(" = new ArrayList<>(Arrays.asList());") + Key("left:3"),
        "(array | hooray) list [<text>]": Function(defineArrayList),
        "hash map [<text>]": Function(defineHashMap),

        # "cast to integer": Text("(int)()")+ Key("left"),
        "big integer": Text("Integer "),
        "string": Text("String "),
        "becomes": Text(" -> "),
        
        # "substring": Text("substring"),
        "(short | sue) if then": Text("if ()")+ Key("left"),
        "(short | sue) shells": Text("else")+ Key("enter"),
        "(shell | shells) if": Text("else if ()")+ Key("left"),

        "ternary": Text("()?:") + Key("left:3"),
        # "throw exception": Text("throw new Exception()")+ Key("left"),
        # "is instance of": Text(" instanceof "),
        "is instance of": Key("dot, i, n, s, t/" + INTELLIJ_POPUP_DELAY + ", enter"),

        specs.SymbolSpecs.NEW: Text("new "),
        "new me up": Key("space, equal, space, n, e, w, space/10, cs-space"),
        "this": Text("this"),
        "continue": Text("continue"),
        "public": Text("public "),
        "private": Text("private "),
        "static": Text("static "),
        "final": Text("final "),
        "void": Text("void "),
        "abstract": Text("abstract "),
        "assert": Text("assert "),
        "go to": Text("goto "),
        "package": Text("package "),
        "synchronized": Text("synchronized "),
        "double": Text("double "),
        "implements": Text("implements "),
        "import": Text("import "),
        "throws": Text("throws "),
        "throw": Text("throw new "),
        "enumeration": Text("enum "),
        "transient": Text("transient "),
        "extends": Text("extends "),
        "try": Text("try "),
        "catch": Text("catch "),
        "interface": Text("interface "),
        "finally": Text("finally "),
        "volatile": Text("volatile "),
        "constant": Text("const "),
        "native": Text("native "),
        "super": Text("super "),

        "(bite | byte)": Text("byte "),
        "(integer | int)": Text("int "),
        "boolean": Text("boolean "),
        "(character | char)": Text("char "),
        "short": Text("short "),
        "long": Text("long "),
        "float": Text("float "),
        "char": Text("char "),
    }
    extras = [
        Dictation("modifiers"),
        Dictation("text"),
    ]
    defaults = {
        "modifiers": None,
        "text": None,
    }

