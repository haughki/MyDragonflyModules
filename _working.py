# import sys
# sys.path.append('pycharm-debug.egg')
# import pydevd
# pydevd.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)

import inspect
from hawk.method_builder import method_builder
from dragonfly import *

import logging

from dragonfly import log

log.setup_log()
# log.setup_tracing()

from dragonfly.actions.action_function import Function
from dragonfly.actions.action_key import Key
from dragonfly.actions.action_text import Text
from dragonfly.grammar.elements_basic import Dictation
from dragonfly.grammar.rule_mapping import MappingRule

__author__ = 'parkerh'


class ProgrammingLanguage(object):
    def __init__(self, name):
        self._name = name

    def getName(self):
        return self._name

    def goPrint(self):
        pass

    def goMethod(self, modifiers=None):
        pass

    def goForLoop(self):
        Text("for (:){").execute()
        Key("enter, up").execute()


# This method list will be used below to auto generate and dynamically bind
# "copies" of the methods in ProgrammingLanguage. Ultimately, we do this
# so that we can use voice commands to invoke the desired method.
method_list = inspect.getmembers(ProgrammingLanguage, inspect.ismethod)


class Python(ProgrammingLanguage):
    def __init__(self):
        super(Python, self).__init__("python")

    def goPrint(self):
        Text("print ").execute()

    def goMethod(self, modifiers=None):
        Text("def (self):").execute()
        Key("left:7").execute()

    def goForLoop(self):
        Text("for in :").execute()
        Key("left:4").execute()


class CSharp(ProgrammingLanguage):
    def __init__(self):
        super(CSharp, self).__init__("csharp")

    def goPrint(self):
        Text("Console.WriteLine()").execute()
        Key("left").execute()

    def goMethod(self, modifiers=None):
        if modifiers is None:
            modifiers = "private"
        else:
            modifiers = str(modifiers).lower()

        Text(modifiers + " void a()").execute()
        Key("enter, lbrace, enter, up:2, ctrl:down, right:" + str(
            len(modifiers.split(" ")) + 1) + ", ctrl:up, del").execute()


class Java(ProgrammingLanguage):
    def __init__(self):
        super(Java, self).__init__("java")

    def goPrint(self):
        Text("System.out.println(").execute()
        # Key("left").execute()

    def goMethod(self, modifiers=None):
        print modifiers
        if modifiers is None:
            modifiers = "private"
        else:
            modifiers = str(modifiers).lower()

        Text(modifiers + " void a()").execute()
        Key("enter, lbrace, enter, up:2, ctrl:down, right:" + str(
            len(modifiers.split(" ")) + 1) + ", ctrl:up, del").execute()


class SupportedLanguages(object):
    def __init__(self):
        self._langList = {Python().getName(): Python(),
                          CSharp().getName(): CSharp(),
                          Java().getName(): Java(),
                          }

    def getLanguageList(self):
        return self._langList


class LanguageContext(object):
    """ creates a programming language-specific context, so that the same command will insert
    different code snippets depending on the current language context.
    """

    def __init__(self, supportedLanguages):
        self._current = None
        self._supported = supportedLanguages.getLanguageList()
        self.setCurrentLanguage("java")

    def getCurrentLanguage(self):
        return self._current

    def getCurrentLanguageName(self):
        return self._current.getName()

    def printCurrentLanguageName(self):
        print self._current.getName()

    def setCurrentLanguage(self, lang):  # lang is a Dictation object. str'ing it gets the dictation
        languageAsString = str(lang).lower().replace(" ", "")
        self.validateLanguage(languageAsString)
        self._current = self._supported[languageAsString]

    def isEnabled(self):
        if self._current is None:
            print "WARNING:  No programming langauge context is defined!"
            return False
        return True

    def validateLanguage(self, lang):
        isSupported = False
        for supported in self._supported.keys():
            if supported == lang:
                isSupported = True
                break

        if not isSupported:
            raise StandardError("Unsupported language: " + lang)

    def addPassThroughMethods(self):
        """ Auto generates 'mapping methods' based on all of the methods in ProgrammingLanguage. These will, 
        in turn, map to corresponding methods in the global scope (see method_builder at global scope). Ultimately, 
        we do all this so that we can use voice commands to invoke the desired method.  E.g., given the 
        ProgrammingLanguage definition:
            
            def goPrint(self):
            
        The following code will dynamically add a new method to this class, defined as:
        
            def goPrint(self):
                self._current.goPrint()
        """
        from types import MethodType  # LEAVE THIS -- used by auto-generated code
        codelist = method_builder(method_list, "self._current", True)
        for code in codelist:
            exec code

        for method in method_list:
            if not method[0] == "__init__":
                exec "LanguageContext." + method[0] + " = MethodType(" + method[0] + ", None, LanguageContext)"


language = LanguageContext(SupportedLanguages())
language.addPassThroughMethods()

# Auto generates 'mapping functions' based on all of the methods in ProgrammingLanguage.  The mapping dictionary
# within InsertCodeRule will reference these functions in its map. Originally, I had been directly referencing
# the methods within LanguageContext from the InsertCodeRule map. This wasn't working: my sense is that the 
# Function() methods within the InsertCodeRule map capture the state of the passed function (as a closure).  So,
# I needed to add a level of indirection at the global scope.  E.g., given the ProgrammingLanguage definition:
# 
# def goPrint(self):
# 
# The following code will dynamically add a new function to this module, defined as:
#
# def goPrint():
#    language.goPrint()

codelist = method_builder(method_list, "language", False)
for code in codelist:
    exec code


class InsertCodeRule(MappingRule):
    mapping = {
        # "run inspector": Function(inspector),
        "go print": Function(goPrint),  # the function referenced here (and below) are dynamically added -- hence the "error" highlighting
        "go [<modifiers>] method": Function(goMethod),
        "go for loop": Function(goForLoop),
        # the dictation object gets passed to setLanguage as the "lang" param via extras below.  builtin to Function
        "set language <lang>": Function(language.setCurrentLanguage),
        "get [current] language": Function(language.printCurrentLanguageName),
    }

    extras = [
        Dictation("lang"),
        Dictation("modifiers"),
    ]

    defaults = {
        "modifiers": None,
    }


a_rule = InsertCodeRule()
grammar = Grammar("example grammar")
grammar.add_rule(a_rule)
grammar.load()


def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
