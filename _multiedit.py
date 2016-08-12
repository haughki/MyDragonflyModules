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
from hawk import insertcode
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
        {
    },
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

if insertcode.InsertCodeRule:
    alternatives.append(RuleRef(rule=insertcode.InsertCodeRule()))

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
                    if commands[action_loop_count] == "mash":  # special command to uppercase individual letters
                        if len(sequence) > 1:
                            upper_case_it = sequence[action_loop_count] + sequence[action_loop_count + 1] + release
                            upper_case_it.execute()
                            is_skip_next_action = True
                    else:
                        action.execute()
                else:
                    action.execute()


#---------------------------------------------------------------------------
# Create and load this module's grammar.

grammar = Grammar("multi edit")   # Create this module's grammar.
grammar.add_rule(RepeatRule())    # Add the top-level rule.
grammar.load()                    # Load the grammar.

# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
