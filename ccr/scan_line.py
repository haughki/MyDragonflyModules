from dragonfly import Function, MappingRule, Text, Dictation, Key
from supporting import utils, character


def lineSearch(dictation_to_find, replace_with_me, _node):
    commands = _node.words()

    # parse ordinal arguments
    second_arg = commands[1]
    ordinal_arg = None
    for ordinal in ordinal_map:
        if second_arg == ordinal:
            ordinal_arg = second_arg
            break

    # parse replace arguments
    replacing = False
    if len(commands) > 2:
        second_to_last_arg = commands[-2]
        last_arg = commands[-1]
        if second_to_last_arg == "replace" or last_arg == "replace":
            print "Replacing..."
            replacing = True
            replace_with_me = str(replace_with_me)

    to_find = str(dictation_to_find)
    if to_find == "":
        print "No dictation, searching for character..."
        character_to_find = _node.words()[-1]
        to_find = character.CHARACTER_MAP[character_to_find]

    to_find = to_find.lower()
    searching_message = "Searching for " + ordinal_arg + ": "  if ordinal_arg else "Searching for: "
    print searching_message + to_find
    Key("end,s-home/5").execute()  # select the line
    line = utils.getSelectedText().lower()  # copied to the clipboard, then get from the clipboard
    print "Searching in line: " + line
    line_index = -1
    if ordinal_arg:
        line_index = utils.find_nth(line, to_find, ordinal_map[ordinal_arg])
    else:
        line_index = line.find(to_find)
    if line_index != -1:
        Key("end,home,right:" + str(line_index)).execute()
        if replacing:
            Key("cs-right").execute()
            selected = utils.getSelectedText()
            if selected[-1] == " ":
                Key("s-left").execute()  # deselect a single trailing space if it exists
            if replace_with_me == "":
                Key("backspace").execute()
            else:
                Text(replace_with_me).execute()
    else:
        Key("escape").execute()
        print "unable to find: " + to_find
        print "line: " + line


ordinal_map = {"second":2, "third":3, "fourth":4, "fifth":5, "sixth":6}

class ScanLineRule(MappingRule):
    mapping = {
        "scan [(second | third | fourth | fifth | sixth)] (<dictation_to_find> | " + character.CHARACTER_ALTERNATIVES + ") [replace] [<replace_with_me>]": Function(lineSearch),
    }

    extras = [Dictation("dictation_to_find"),
              Dictation("replace_with_me"),
              ]
    defaults = {"dictation_to_find":"",
                "replace_with_me":"",
                }
