'''
Created on Oct 17, 2015
@author: synkarius
'''
import re


class TokenSet(object):
    SYMBOL_PATTERN = re.compile("([A-Za-z0-9_]+)")
    def __init__(self, keywords, line_comment, long_comment):
        self.keywords = keywords
        self.line_comment = line_comment
        self.long_comment = long_comment

class SymbolSpecs(object):
    IF = "if then"
    ELSE = "(shells | else)"
    DEFINE_METHOD = "[(public | protected | private)] [static] [final] [void] method [pascal | snake] [<text>]"  # public static void myMethod()
    
    SWITCH = "switch statement"
    CASE = "case of"
    BREAK = "breaker"
    DEFAULT = "default"
    
    DO_LOOP = "do loop"
    WHILE_LOOP = "while loop"
    FOR_EACH_LOOP = "for each"
    FOR_LOOP = "for loop"
    TRY_CATCH = "try catch"

    TO_INTEGER = "to integer"
    TO_FLOAT = "to floating point"
    TO_STRING = "to string"
    
    AND = "lodge and"
    OR = "lodge or"
    NOT = "lodge not"
    
    SYSOUT = "print out"
    IMPORT = "import"
    FUNCTION = "function"
    CLASS = "[(public | protected | private)] [static] [final] class [camel | snake] [<text>]"
    
    COMMENT = "add comment"
    LONG_COMMENT = "long comment"
    
    NOT_EQUAL_NULL = "not nothing"
    NULL = "(null | nothing)"
    RETURN = "return"
    TRUE = "true"
    FALSE = "false"
    NEW = "new"