# import sys
# sys.path.append('pycharm-debug.egg')
# import pydevd
# pydevd.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)

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

    def goPrint(self):
        self._current.goPrint()

    def goMethod(self, modifiers):
        self._current.goMethod(modifiers)

    def goForLoop(self):
        self._current.goForLoop()


language = LanguageContext(SupportedLanguages())

# exec ("""def goPrint(): language.goPrint()""")


# def goMethod(modifiers=None):
#     language.goMethod(modifiers)
# 
# def goForLoop():
#     language.goForLoop()



import inspect
from pprint import pprint

method_list = inspect.getmembers(ProgrammingLanguage, inspect.ismethod)
for method in method_list:
    print method[0]
    current_method_name = method[0]
    if not current_method_name == "__init__":
        code = "def " + current_method_name + "(): language." + current_method_name + "()"
        argument_specification = inspect.getargspec(method[1])
        if argument_specification.args:
            arguments = argument_specification.args
            arguments_with_defaults = None
            if not (len(arguments) == 1 and arguments[0] == "self"):
                # we have some arguments to deal with
                print argument_specification
                if argument_specification.defaults:
                    defaults = argument_specification.defaults
                    arguments_which_have_defaults = arguments[-len(defaults):]
                    arguments_with_defaults = zip(arguments_which_have_defaults, defaults)
                    if len(arguments) >= len(arguments_with_defaults):
                        arguments = arguments[:-len(defaults)]  # we have some defaults, so remove those from the list of arguments -- need to deal with those separately

                print arguments
                print arguments_with_defaults

                argument_list = ""
                argument_list_with_defaults = ""
                for argument in arguments:
                    if argument != "self":
                        argument_list = argument_list + argument + ", "

                argument_list_with_defaults = argument_list
                for default_argument in arguments_with_defaults:
                    argument_list_with_defaults = argument_list_with_defaults + default_argument[0] + "=" + str(default_argument[1]) + ", "
                    argument_list = argument_list + default_argument[0] + ", "

                if argument_list[-2] == ",":
                    argument_list = argument_list[:-2]
                if argument_list_with_defaults[-2] == ",":
                    argument_list_with_defaults = argument_list_with_defaults[:-2]

                print argument_list
                print argument_list_with_defaults
                code = "def " + current_method_name + "(" + argument_list_with_defaults + "): language." + current_method_name + "(" + argument_list + ")"

        print code
        exec code

# for method in method_list:
#     # print method[0]
#     current_method_name = method[0]
#     if not current_method_name == "__init__":
#         code = "def " + current_method_name + "(): language." + current_method_name + "()"
#         # print code
#         exec (code)


# def inspector():
#     method_list = inspect.getmembers(ProgrammingLanguage, inspect.ismethod)
#     for method in method_list:
#         print method[0]
#         current_method_name = method[0]
#         if not current_method_name == "__init__":
#             code = "def " + current_method_name + "(): language." + current_method_name + "()"
#             argument_specification = inspect.getargspec(method[1])
#             if argument_specification.args:
#                 arguments = argument_specification.args
#                 arguments_with_defaults = None
#                 if not (len(arguments) == 1 and arguments[0] == "self"):
#                     # we have some arguments to deal with
#                     print argument_specification
#                     if argument_specification.defaults:
#                         defaults = argument_specification.defaults
#                         arguments_which_have_defaults = arguments[-len(defaults):]
#                         arguments_with_defaults = zip(arguments_which_have_defaults, defaults)
#                         if len(arguments) >= len(arguments_with_defaults):
#                             arguments = arguments[:-len(defaults)]  # we have some defaults, so remove those from the list of arguments -- need to deal with those separately
# 
#                     print arguments
#                     print arguments_with_defaults
#                     
#                     argument_list = ""
#                     for argument in arguments:
#                         if argument != "self":
#                             argument_list = argument_list + argument + ", "
#                     
#                     for default_argument in arguments_with_defaults:
#                         argument_list = argument_list + default_argument[0] + "=" + str(default_argument[1]) + ", "
#                         
#                     if argument_list[-2] == ",":
#                         argument_list = argument_list[:-2]
#                     print argument_list
#                     code = "def " + current_method_name + "(" + argument_list + "): language." + current_method_name + "(" + argument_list + ")"
#                     
#             print code
#             # exec (code)


class InsertCodeRule(MappingRule):
    mapping = {
        # "run inspector": Function(inspector),
        "go print": Function(goPrint),
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
