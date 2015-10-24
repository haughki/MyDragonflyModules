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

    def goMethod(self, modifiers):
        pass


class Python(ProgrammingLanguage):
    def __init__(self):
        super(Python, self).__init__("python")

    def goPrint(self):
        Text("print ").execute()

    def goMethod(self, modifiers=None):
        Text("def (self):").execute()
        Key("left:7").execute()


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


class SupportedLanguages(object):
    def __init__(self):
        self._langList = {Python().getName(): Python(),
                          CSharp().getName(): CSharp(),
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

    def getCurrentLanguage(self):
        return self._current

    def setCurrentLanguage(self, lang): # lang is a Dictation object. str'ing it gets the dictation
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
        if not self.isEnabled():
            return
        self._current.goPrint()

    def goMethod(self, modifiers):
        if not self.isEnabled():
            return
        self._current.goMethod(modifiers)


language = LanguageContext(SupportedLanguages())


def setLanguage(lang):
    language.setCurrentLanguage(lang)


def getLanguage():
    print language.getCurrentLanguage()


def goPrint():
    language.goPrint()


def goMethod(modifiers=None):
    language.goMethod(modifiers)


class InsertCodeRule(MappingRule):
    mapping = {
        "go print": Function(goPrint),
        "go [<modifiers>] method": Function(goMethod),
        # the dictation object gets passed to setLanguage as the "lang" param via extras below.  builtin to Function
        "set language <lang>": Function(setLanguage),
        "get current language": Function(getLanguage),
        }

    extras = [
        Dictation("lang"),
        Dictation("modifiers"),
        ]

    defaults = {
        "modifiers": None,
        }

