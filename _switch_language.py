#---------------------------------------------------------------------------
# language section
# section for defining language-specific commands and outputs
# 
from dragonfly import Dictation
from dragonfly import Function
from dragonfly import MappingRule

from languages import _java_rule, _python_rule


class SupportedLanguages(object):
    def __init__(self):
        self._langList = {_python_rule.PythonRule.get_name(): _python_rule.python_grammar,
                          _java_rule.JavaRule.get_name(): _java_rule.java_grammar,
                          }


    def getLanguageList(self):
        return self._langList


class LanguageContext(object):
    """ creates a programming language-specific context, so that the same command will insert
    different code snippets depending on the current language context.
    """

    def __init__(self, supportedLanguages):
        self._current = None
        self._current_name = "No language name set!?"
        self._supported = supportedLanguages.getLanguageList()

        # start with everything disabled
        for k in self._supported:
            self._supported[k].disable()

        self.setCurrentLanguage("python")

    def printCurrentLanguageName(self):
        print self._current_name

    def setCurrentLanguage(self, lang):  # lang is a Dictation object. str'ing it gets the dictation
        languageAsString = str(lang).lower().replace(" ", "")
        self.validateLanguage(languageAsString)
        if self._current:
            self._current.disable()
        self._current = self._supported[languageAsString]
        self._current.enable()
        self._current_name = languageAsString

    def validateLanguage(self, lang):
        isSupported = False
        for supported in self._supported.keys():
            if supported == lang:
                isSupported = True
                break
        if not isSupported:
            raise StandardError("Unsupported language: " + lang)


language = LanguageContext(SupportedLanguages())

class SwitchLanguageRule(MappingRule):
    exported = False
    mapping = {
        # the dictation object gets passed to setLanguage as the "lang" param via "extras" below.  builtin to Function
        "set language <lang>": Function(language.setCurrentLanguage),
        "get [current] language": Function(language.printCurrentLanguageName),
    }

    extras = [
        Dictation("lang"),
    ]
    
