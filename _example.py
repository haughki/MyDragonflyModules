# import sys
# sys.path.append('pycharm-debug.egg')
# import pydevd
# pydevd.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)



from dragonfly import *

from supporting import utils, character


ordinal_map = {"second":2, "third":3, "fourth":4, "fifth":5, "sixth":6}

class Example(CompoundRule):
    spec = "look [(second | third | fourth | fifth | sixth)] (<text> | " + character.CHARACTER_OPTIONS + ")"

    extras = [Dictation("text"),
              ]
    defaults = {"text":""}

    def _process_recognition(self, node, extras):
        second_arg = node.words()[1]
        ordinal_arg = None
        for ordinal in ordinal_map:
            if second_arg == ordinal:
                ordinal_arg = second_arg
                break
                        
        to_find = str(extras["text"])
        if to_find == "":
            print "No dictation, searching for character..."
            character_to_find = node.words()[-1]
            to_find = character.CHARACTER_MAP[character_to_find]
        
        to_find = to_find.lower()
        searching_message = "Searching for " + ordinal_arg + ": "  if ordinal_arg else "Searching for: " 
        print searching_message + to_find 
        Key("end,s-home").execute()  # select the line
        line = utils.getSelectedText().lower()  # copied to the clipboard, then get from the clipboard 
        line_index = -1
        if ordinal_arg:
            line_index = utils.find_nth(line, to_find, ordinal_map[ordinal_arg])
        else:
            line_index = line.find(to_find)
        if line_index != -1:
            Key("end,home,right:" + str(line_index)).execute()
        else:
            Key("escape").execute()
            print "unable to find: " + to_find
            print "line: " + line


example_grammar = Grammar("example grammar")
example_grammar.add_rule(Example())


example_grammar.load()

def unload():
    global example_grammar
    if example_grammar:
        print "unloading " + __name__ + "..."
        example_grammar.unload()
    example_grammar = None
