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
    DEFINE_METHOD = "define [(public | protected | private)] [static] [void] method"  # public static void myMethod()
    
    SWITCH = "switch"
    CASE = "case of"
    BREAK = "breaker"
    DEFAULT = "default"
    
    DO_LOOP = "do loop"
    WHILE_LOOP = "while loop"
    FOR_EACH_LOOP = "for each"
    FOR_LOOP = "for loop"

    TO_INTEGER = "to integer"
    TO_FLOAT = "to floating point"
    TO_STRING = "to string"
    
    AND = "lodge and"
    OR = "lodge or"
    NOT = "lodge not"
    
    SYSOUT = "print statement"
    
    IMPORT = "import"
    
    FUNCTION = "function"
    CLASS = "class"
    
    COMMENT = "add comment"
    LONG_COMMENT = "long comment"
    
    NULL = "value not"
    
    RETURN = "return"
    
    TRUE = "value true"
    FALSE = "value false"

    # not part of the programming standard:
    CANCEL = "(terminate | escape)"
    