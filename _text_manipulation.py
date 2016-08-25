#
# This file is a command-module for Dragonfly.
# (c) Copyright 2016 by Hawkeye Parker
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for manipulating text
=====================================================

This command-module offers commands for manipulating text.

Commands
--------

The following voice commands are available:

Command: **"upper that"**
    Converst the selected text to upper case


Usage examples
--------------

 - Say **"upper that"** to convert the selected text to upper case.

"""

# import logging
from dragonfly.windows.clipboard import Clipboard
from dragonfly import Config, Section, Item, Grammar, CompoundRule, Key
from supporting import utils

# rule_log = logging.getLogger("rule")

# ---------------------------------------------------------------------------
# Set up this module's configuration.

config = Config("Text Manipulation")
config.tweak = Section("Tweak section")
config.tweak.upper = Item("upper that", doc="Command to convert the selected text to uppercase.")
config.tweak.lower = Item("lower that", doc="Command to convert the selected text to lower case.")
# config.generate_config_file()
config.load()

# ===========================================================================
# Create this module's main grammar object.

grammar = Grammar("text manipulation")


class UpperRule(CompoundRule):
    spec = config.tweak.upper

    def _process_recognition(self, node, extras):
        copy_modify_paste(lambda s: s.upper())

grammar.add_rule(UpperRule())


class LowerRule(CompoundRule):
    spec = config.tweak.lower

    def _process_recognition(self, node, extras):
        copy_modify_paste(lambda s: s.lower())

grammar.add_rule(LowerRule())


# ---------------------------------------------------------------------------

def copy_modify_paste(modifying_function):
    selected_text = utils.getSelectedText()
    if not selected_text:
        print "No selected text?"
        return
    modified_text = modifying_function(str(selected_text))
    # tried to use the original clipboard here, but couldn't get it to "clear" -- some apps would
    # somehow get the original, unmodified text when the paste happened
    new_clipboard = Clipboard()
    new_clipboard.set_text(modified_text)
    new_clipboard.copy_to_system()
    Key("c-v").execute()


grammar.load()


def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
