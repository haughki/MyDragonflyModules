#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for cursor movement and **editing**
============================================================================

This module allows the user to control the cursor and efficiently perform multiple text editing actions within a
single phrase.


Example commands
----------------------------------------------------------------------------

*Note the "/" characters in the examples below are simply to help the reader see the different parts of each voice
command.  They are not present in the actual command and should not be spoken.*

Example: **"up 4 / down 1 page / home / space 2"**
   This command will move the cursor up 4 lines, down 1 page, move to the beginning of the line, and then insert 2 spaces.

Example: **"left 7 words / backspace 3 / insert hello Cap world"**
   This command will move the cursor left 7 words, then delete the 3 characters before the cursor, and finally insert
   the text "hello World".

Example: **"home / space 4 / down / 43 times"**
   This command will insert 4 spaces at the beginning of this and the next 42 lines.  The final "43 times"
   repeats everything in front of it that many times.


Discussion of this module
----------------------------------------------------------------------------

This command-module creates a powerful voice command for editing and cursor movement.  This command's structure can
be represented by the following simplified language model:

 - *CommandRule* -- top-level rule which the user can say
    - *repetition* -- sequence of actions (name = "sequence")
       - *KeystrokeRule* -- rule that maps a single 
         spoken-form to an action
    - *optional* -- optional specification of repeat count
       - *integer* -- repeat count (name = "n")
       - *literal* -- "times"

The top-level command rule has a callback method which is called when this voice command is recognized.  The logic
within this callback is very simple:

1. Retrieve the sequence of actions from the element with the name "sequence".
2. Retrieve the repeat count from the element with the name "n".
3. Execute the actions the specified number of times.

"""
try:
    import pkg_resources

    pkg_resources.require("dragonfly >= 0.6.5beta1.dev-r99")
except ImportError:
    pass

from dragonfly import *
# from hawk import insertcode
from hawk import putstringcommands

#---------------------------------------------------------------------------
# Here we globally defined the release action which releases all modifier-keys used within this grammar.  It is defined here
#  because this functionality is used in many different places. Note that it is harmless to release ("...:up") a key multiple
#  times or when that key is not held down at all.

release = Key("shift:up, ctrl:up, alt:up")


#---------------------------------------------------------------------------
# Set up this module's configuration.

config = Config("multi edit")
config.cmd = Section("Command section")
config.cmd.map = Item(
    # Here we define the *default* command map.  If you would like to modify it to your personal taste, please *do not* make changes
    #  here.  Instead change the *config file* called "_multiedit.txt".
    {},
    namespace={
        "Key": Key,
        "Text": Text,
        }
)
namespace = config.load()

#---------------------------------------------------------------------------
# Here we prepare the list of formatting functions from the config file.

# Retrieve text-formatting functions from this module's config file. Each of these functions must have a name that starts with "format_".
format_functions = {}
if namespace:
    for name, function in namespace.items():
        if name.startswith("format_") and callable(function):
            spoken_form = function.__doc__.strip()

            # We wrap generation of the Function action in a function so that its *function* variable will be local.  Otherwise it
            #  would change during the next iteration of the namespace loop.
            def wrap_function(function):
                def _function(dictation):
                    formatted_text = function(dictation)
                    Text(formatted_text).execute()

                return Function(_function)

            action = wrap_function(function)
            format_functions[spoken_form] = action


# Here we define the text formatting rule. The contents of this rule were built up from the "format_*"
#  functions in this module's config file.
if format_functions:
    class FormatRule(MappingRule):
        mapping = format_functions
        extras = [Dictation("dictation")]

else:
    FormatRule = None


#---------------------------------------------------------------------------
# language section
# section for defining language-specific commands and outputs
# 

import inspect
from hawk.method_builder import method_builder
# from dragonfly import *
from dragonfly.actions.action_function import Function
from dragonfly.actions.action_key import Key
from dragonfly.actions.action_text import Text
from dragonfly.grammar.elements_basic import Dictation
from dragonfly.grammar.rule_mapping import MappingRule

__author__ = 'parkerh'


class ProgrammingLanguage(object):
    """ Abstract base class. Implementations are Java syntax. """
    def __init__(self, name):
        self._name = name

    def getName(self):
        return self._name

    def goPrint(self):
        pass

    def goMethod(self, modifiers=None):
        if modifiers is None:
            modifiers = "private"
        else:
            modifiers = str(modifiers).lower()

        Text(modifiers + " void a()").execute()
        Key("enter, lbrace, enter, up:2, ctrl:down, right:" + str(
            len(modifiers.split(" ")) + 1) + ", ctrl:up, del").execute()

    def goForLoop(self):
        Text("for (:){").execute()
        Key("enter, up").execute()

    def lineComment(self):
        Text("// ").execute()

    def ifThen(self):
        Text("if (){").execute()
        Key("enter, up, right:4").execute()


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


class Java(ProgrammingLanguage):
    def __init__(self):
        super(Java, self).__init__("java")

    def goPrint(self):
        Text("System.out.println(").execute()
        # Key("left").execute()


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
    exported = False
    mapping = {
        # "run inspector": Function(inspector),
        "go print": Function(goPrint),  # the function referenced here (and below) are dynamically added -- hence the "error" highlighting
        "go [<modifiers>] method": Function(goMethod),
        "go for loop": Function(goForLoop),
        "line comment": Function(lineComment),
        "if then": Function(ifThen),
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









#---------------------------------------------------------------------------
# Here we define the keystroke rule.

# This rule maps spoken-forms to actions.  Some of these include special elements like the number with name "n"
#  or the dictation with name "text".  This rule is not exported, but is referenced by other elements later on.
#  It is derived from MappingRule, so that its "value" when processing a recognition will be the right side of the
#  mapping: an action.
# Note that this rule does not execute these actions, it simply returns them when it's value() method is called.
#  For example "up 4" will give the value Key("up:4"). This is default behavior of the MappingRule class' value() method.  It also
#  substitutes any "%(...)." within the action spec with the appropriate spoken values.
class KeystrokeRule(MappingRule):
    exported = False

    mapping = config.cmd.map
    extras = [
        IntegerRef("n", 1, 100),
        Dictation("text"),
        Dictation("text2"),
        ]
    defaults = {
        "n": 1,
        }


#---------------------------------------------------------------------------
# Here we create an element which is the sequence of keystrokes.

# First we create an element that references the keystroke rule. Note: when processing a recognition, the *value* of this element
#  will be the value of the referenced rule: an action.
alternatives = []
alternatives.append(RuleRef(rule=KeystrokeRule()))
if FormatRule:
    alternatives.append(RuleRef(rule=FormatRule()))

if InsertCodeRule:
    alternatives.append(RuleRef(rule=InsertCodeRule()))

if putstringcommands.PutStringCommandsRule:
    alternatives.append(RuleRef(rule=putstringcommands.PutStringCommandsRule()))

single_action = Alternative(alternatives)

# Second we create a repetition of keystroke elements. This element will match anywhere between 1 and 16 repetitions
#  of the keystroke elements.  Note that we give this element the name "sequence" so that it can be used as an extra in
#  the rule definition below.
# Note: when processing a recognition, the *value* of this element will be a sequence of the contained elements: a sequence of
#  actions.
sequence = Repetition(single_action, min=1, max=16, name="sequence")


#---------------------------------------------------------------------------
# Here we define the top-level rule which the user can say.

# This is the rule that actually handles recognitions. When a recognition occurs, it's _process_recognition()
#  method will be called.  It receives information about the recognition in the "extras" argument: the sequence of
#  actions and the number of times to repeat them.
class RepeatRule(CompoundRule):
    # Here we define this rule's spoken-form and special elements.
    spec = "<sequence> [[[and] repeat [that]] <n> times]"
    extras = [
        sequence, # Sequence of actions defined above.
        IntegerRef("n", 1, 100), # Times to repeat the sequence.
    ]
    defaults = {
        "n": 1, # Default repeat count.
    }

    # This method gets called when this rule is recognized.
    #  - node -- root node of the recognition parse tree.
    #  - extras -- dict of the "extras" special elements:
    #     . extras["sequence"] gives the sequence of actions.
    #     . extras["n"] gives the repeat count.
    def _process_recognition(self, node, extras):
        sequence = extras["sequence"]   # A sequence of actions.
        repeat_count = extras["n"]      # An integer repeat count.
        #print sequence
        is_skip_next_action = False
        for i in range(repeat_count):
            action_loop_count = -1
            for action in sequence:
                # all of the "extra" code below is for the "mash" command
                action_loop_count += 1
                #print ""
                #print action_loop_count
                #print is_skip_next_action
                #print action
                if is_skip_next_action:
                    is_skip_next_action = False
                    continue
                #print node.words()
                commands = node.words()
                if len(commands) > 0:
                    if commands[action_loop_count] == "mash" or commands[action_loop_count] == "sky":  # special command to uppercase individual letters
                        if len(sequence) > 1:
                            upper_case_it = sequence[action_loop_count] + sequence[action_loop_count + 1] + release
                            upper_case_it.execute()
                            is_skip_next_action = True
                    else:
                        action.execute()
                else:
                    action.execute()


class ReloadRule(CompoundRule):
    spec = "reload code insert"                  # Spoken form of command.

    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        print "reloading code insert..."
        # reload(insertcode)


#---------------------------------------------------------------------------
# Create and load this module's grammar.

grammar = Grammar("multi edit")   # Create this module's grammar.
grammar.add_rule(RepeatRule())    # Add the top-level rule.
grammar.add_rule(ReloadRule())
grammar.load()                    # Load the grammar.

# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
