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

    pkg_resources.require("dragonfly2 >= 0.6.5beta1.dev-r99")
except ImportError:
    pass

from dragonfly import *
from supporting import character


""" Converts a lowercase char to uppercase. The 'letters_ref' is defined in the 'extras' of the mapping rule.
    The 'ref' makes it possible to pass the dictated value (e.g., "Alpha") to this Function action."""
def convert_to_upper(letters_ref):  # Note, the parameter name here has to match the value of the 'name' member of the ListRef.
    Key(letters_ref).execute()

letters = List("letters_list", [
    character.A, character.B, character.C, character.D, character.E, character.F, character.G, character.H, character.I, character.J, character.K, character.L, character.M, character.N, character.O, character.P, character.Q, character.R, character.S, character.T, character.U, character.V, character.W, character.X, character.Y, character.Z
])
letters_reference = ListRef("letters_ref", letters)

#---------------------------------------------------------------------------
# Here we globally defined the release action which releases all modifier-keys used within this grammar.  It is defined here
#  because this functionality is used in many different places. Note that it is harmless to release ("...:up") a key multiple
#  times or when that key is not held down at all.
release = Key("shift:up, ctrl:up, alt:up")

#---------------------------------------------------------------------------
# Here we define the keystroke rule.

# This rule maps spoken-forms to actions.  Some of these include special elements like the number with name "n" or the dictation
# with name "text". It is derived from MappingRule, so that its "value" when processing a recognition will be the right side of the
# mapping: an action.
# Note that this rule does not execute these actions, it simply returns them when it's value() method is called.
# For example "up 4" will give the value Key("up:4"). This is default behavior of the MappingRule class' value() method.  It also
# substitutes any "%(...)." within the action spec with the appropriate spoken values.
class MultiEditRule(MappingRule):
    exported = False

    #---------------------------------------------------------------------------
    # Here we define the single-action commands.  These can be spoken
    #  in series so as to execute multiple actions within a single utterance.
    mapping = {
        # Spoken-form    ->    ->    ->     Action object

        #### Dragon
        "Snork": Key("npadd/10,npadd"),  # turn mic on and off
        "(Mike | mic) off": Key("npadd"),  # turn mic off
        "sleep": Key("npdiv"),

        #### Cursor manipulation
        "cup [<n>]": Key("up:%(n)d"),
        "down [<n>]": Key("down:%(n)d"),
        "left [<n>]": Key("left:%(n)d"),
        "right [<n>]": Key("right:%(n)d"),
        "tope [<n>]": Key("pgup:%(n)d"),
        "drop [<n>]": Key("pgdown:%(n)d"),
        "(port | Lefty | word left) [<n>]": Key("c-left:%(n)d"),
        "(yope | word right | righty) [<n>]": Key("c-right:%(n)d"),
        "home [<n>]": Key("home:%(n)d"),
        "kick [<n>]": Key("end:%(n)d"),
        "top": Key("c-home"),
        "toe": Key("c-end"),
        "make line": Key("up, end, enter"),
        "(scroll | page) up [<n>]": Key("c-up:%(n)d"),
        "(scroll | page) down [<n>]": Key("c-down:%(n)d"),

        #### Various keys
        character.SPACE       + " [<n>]": Key("space:%(n)d"),
        character.TAB         + " [<n>]": Key("tab:%(n)d"),
        character.S_TAB       + " [<n>]": Key("s-tab:%(n)d"),
        character.ENTER       + " [<n>]": Key("enter:%(n)d"),
        character.DEL         + " [<n>]": Key("del:%(n)d"),
        character.BACKSPACE   + " [<n>]": Key("backspace:%(n)d"),
        character.ESCAPE      + " [<n>]": Key("escape:%(n)d"),

        character.AMPERSAND   + " [<n>]": Key("ampersand:%(n)d"),
        character.APOSTROPHE  + " [<n>]": Key("apostrophe:%(n)d"),
        character.ASTERISK    + " [<n>]": Key("asterisk:%(n)d"),
        character.AT          + " [<n>]": Key("at:%(n)d"),
        character.BACKSLASH   + " [<n>]": Key("backslash:%(n)d"),
        character.BACKTICK    + " [<n>]": Key("backtick:%(n)d"),
        character.BAR         + " [<n>]": Key("bar:%(n)d"),
        character.CARET       + " [<n>]": Key("caret:%(n)d"),
        character.COLON       + " [<n>]": Key("colon:%(n)d"),
        character.HYPHEN      + " [<n>]": Key("hyphen:%(n)d"),
        character.COMMA       + " [<n>]": Key("comma:%(n)d"),
        character.DOLLAR      + " [<n>]": Key("dollar:%(n)d"),
        character.DOT         + " [<n>]": Key("dot:%(n)d"),
        character.DQUOTE      + " [<n>]": Key("dquote:%(n)d"),
        character.EQUAL       + " [<n>]": Key("equal:%(n)d"),
        character.EXCLAMATION + " [<n>]": Key("exclamation:%(n)d"),
        character.HASH        + " [<n>]": Key("hash:%(n)d"),
        character.PERCENT     + " [<n>]": Key("percent:%(n)d"),
        character.PLUS        + " [<n>]": Key("plus:%(n)d"),
        character.QUESTION    + " [<n>]": Key("question:%(n)d"),
        character.SLASH       + " [<n>]": Key("slash:%(n)d"),
        character.SQUOTE      + " [<n>]": Key("squote:%(n)d"),
        character.TILDE       + " [<n>]": Key("tilde:%(n)d"),
        character.UNDERSCORE  + " [<n>]": Key("underscore:%(n)d"),
        character.SEMICOLON   + " [<n>]": Key("semicolon:%(n)d"),
        character.LANGLE      + " [<n>]": Key("langle:%(n)d"),
        character.RANGLE      + " [<n>]": Key("rangle:%(n)d"),
        character.LBRACE      + " [<n>]": Key("lbrace:%(n)d"),
        character.RBRACE      + " [<n>]": Key("rbrace:%(n)d"),
        character.LBRACKET    + " [<n>]": Key("lbracket:%(n)d"),
        character.RBRACKET    + " [<n>]": Key("rbracket:%(n)d"),
        character.LPAREN      + " [<n>]": Key("lparen:%(n)d"),
        character.RPAREN      + " [<n>]": Key("rparen:%(n)d"),

        ### ALPHABET
        character.A           + " [<n>]": Key("a:%(n)d"),
        character.B           + " [<n>]": Key("b:%(n)d"),
        character.C           + " [<n>]": Key("c:%(n)d"),
        character.D           + " [<n>]": Key("d:%(n)d"),
        character.E           + " [<n>]": Key("e:%(n)d"),
        character.F           + " [<n>]": Key("f:%(n)d"),
        character.G           + " [<n>]": Key("g:%(n)d"),
        character.H           + " [<n>]": Key("h:%(n)d"),
        character.I           + " [<n>]": Key("i:%(n)d"),
        character.J           + " [<n>]": Key("j:%(n)d"),
        character.K           + " [<n>]": Key("k:%(n)d"),
        character.L           + " [<n>]": Key("l:%(n)d"),
        character.M           + " [<n>]": Key("m:%(n)d"),
        character.N           + " [<n>]": Key("n:%(n)d"),
        character.O           + " [<n>]": Key("o:%(n)d"),
        character.P           + " [<n>]": Key("p:%(n)d"),
        character.Q           + " [<n>]": Key("q:%(n)d"),
        character.R           + " [<n>]": Key("r:%(n)d"),
        character.S           + " [<n>]": Key("s:%(n)d"),
        character.T           + " [<n>]": Key("t:%(n)d"),
        character.U           + " [<n>]": Key("u:%(n)d"),
        character.V           + " [<n>]": Key("v:%(n)d"),
        character.W           + " [<n>]": Key("w:%(n)d"),
        character.X           + " [<n>]": Key("x:%(n)d"),
        character.Y           + " [<n>]": Key("y:%(n)d"),
        character.Z           + " [<n>]": Key("z:%(n)d"),

        ### Numbers
        "zero": Key("0"),
        "one": Key("1"),
        "two": Key("2"),
        "three": Key("3"),
        "four": Key("4"),
        "five": Key("5"),
        "six": Key("6"),
        "seven": Key("7"),
        "eight": Key("8"),
        "nine": Key("9"),

        ### Function Keys
        "(F | f) one": Key("f1"),
        "(F | f) two": Key("f2"),
        "(F | f) three": Key("f3"),
        "(F | f) four": Key("f4"),
        "(F | f) five": Key("f5"),
        "(F | f) six": Key("f6"),
        "(F | f) seven": Key("f7"),
        "(F | f) eight": Key("f8"),
        "(F | f) nine": Key("f9"),
        "(F | f) ten": Key("f10"),
        "(F | f) eleven": Key("f11"),
        "(F | f) twelve": Key("f12"),

        ### Special Strings
        "gets": Key("space, equal, space"),
        "eeks": Key("space, equal, equal, space"),
        "(not eeks | nodeeks)": Key("space, bang, equal, space"),
        "line dash": Key("space, hyphen, hyphen, space"),
        "(one | won) dash": Key("space, hyphen, space"),
        "string (add | had)": Key("space, plus, space"),
        "(spacebar | space bar) space": Text(" | "),

        ### Lines
        "wipe [<n>]": Key("end, home:2, s-down:%(n)d, del"), # del lines down
        "wipe up [<n>]": release + Key("end, home:2, s-up:%(n)d, s-home, del"), # del lines up
        "clear line": Key("end, home:2, s-end, del"), # del everything on the line except the newline
        "strip": release + Key("s-end, del"), # del from cursor to line end
        "grab": release + Key("s-end, c-c"), # copy from cursor to line end
        "cut end": release + Key("s-end, c-x"), # cut from cursor to line end
        "strip head": release + Key("s-home, del"), # del from cursor to line home
        "grab head": release + Key("s-home, c-c"), # copy from cursor to line home
        "cut head": release + Key("s-home, c-x"), # cut from cursor to line home
        "nab [<n>]": release + Key("end, home:2, s-down:%(n)d, c-c, up"), # copy lines down
        "swipe [<n>]": release + Key("end, home:2, s-down:%(n)d, c-x"), # cut lines down
        "dupe": release + Key("end, home, s-end, c-c, end, enter, c-v"), # duplicate lines down

        ### words
        "bump [<n>]": release + Key("cs-right:%(n)d, del"), # del words right
        "swat [<n>]": release + Key("cs-left:%(n)d, del"), # del words left
        "scoop right [<n>]": release + Key("right:2, c-left, cs-right:%(n)d, c-c, right"), # copy words right
        "scoop left [<n>]": release + Key("left, c-right, cs-left:%(n)d, c-c, left"), # copy words left
        "slice right [<n>]": release + Key("right:2, c-left, cs-right:%(n)d, c-x, right"), # cut words right
        "slice left [<n>]": release + Key("left, c-right, cs-left:%(n)d, c-x, left"), # cut words left
        "select right [<n>]": release + Key("cs-right:%(n)d"), # select words right
        "select left [<n>]": release + Key("cs-left:%(n)d"), # select words left

        ### copy/paste
        "pace": release + Key("c-v"), # paste
        "shell pace": release + Key("cs-v"), # paste into WSL
        "pure pace": release + Key("win:down") + Key("v") + Key("win:up"), # paste without formatting
        "clone [<n>]": release + Key("c-c, c-v:%(n)d"), # copy/paste
        "copy": release + Key("c-c"), # copy
        "shell copy": release + Key("cs-c"), # copy
        "cut": release + Key("c-x"), # cut
        "(select all | tarp)": release + Key("c-a"), # select all

        "(mash | sky <letters_ref>)": Function(convert_to_upper),
        "mark": Key("shift:down"),
        "mark up": Key("shift:up"),
        "release": release,

        ### other
        "control slap": Key("c-enter"),
        "(bolder|boulder) [that]": Key("c-b"),
        "italics [that]": Key("c-i"),
        "undo [<n>]": Key("c-z:%(n)d"),
        "preev window": Key("a-tab/10"),
        "preev file": Key("c-tab"),
        "say <text>": release + Text("%(text)s"),
        "close tab [<n>]": Key("c-w/20:%(n)d"),
        "clean close [<n>]": Key("c-a, del, c-w/20:%(n)d"),
        "new (thing | file)": Key("c-n"),
        "file save": Key("c-s"),
        "file open": Key("c-o"),
        "it'slock": Key("capslock"),

        ### custom vocabulary
        "(bull | T-bull | tex bull | text bull | tex bullet | text bullet)": Text("- "),
        "(slapdash)": Key("enter, hyphen, space"),
    }

    extras = [
        IntegerRef("n", 1, 100),
        Dictation("text"),
        letters_reference,  # see definition of 'convert_to_upper()'
    ]
    defaults = {
        "n": 1,
    }


