# import sys
# sys.path.append('pycharm-debug.egg')
# import pydevd
# pydevd.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)



from dragonfly import *

from supporting import utils
character_map = {"space":" ",
                "amp":"&",
                "star":"*",
                "slosh":"\\",
                "bar":"|",
                "coal":":",
                "dash":"-",
                "drip":",",
                "dot":".",
                "quote":"\"",
                "chud":"=",
                "bang":"!",
                "hash":"#",
                "plus":"+",
                "flash":"/",
                "smote":"'",
                "ray":"_",
                "Shem":";",
                "lang":"<",
                "rang":">",
                "lace":"{",
                "race":"}",
                "lack":"[",
                "rack":"]",
                "lop":"(",
                "hype":")",
                "Al":"a",
                "Braa":"b",
                "Chow":"c",
                "Doy":"d",
                "Eve":"e",
                "Fay":"f",
                "Goo":"g",
                "Hoe":"h",
                "Ice":"i",
                "Jaa":"j",
                "Koi":"k",
                "Lee":"l",
                "Mao":"m",
                "Noy":"n",
                "Oak":"o",
                "Poe":"p",
                "Quinn":"q",
                "Roy":"r",
                "Soy":"s",
                "Tao":"t",
                "Ugh":"u",
                "Vote":"v",
                "Wes":"w",
                "Ecks":"x",
                "Yaa":"y",
                "Zoo":"z",
                "zero":"0",
                "one":"1",
                "two":"2",
                "three":"3",
                "four":"4",
                "five":"5",
                "six":"6",
                "seven":"7",
                "eight":"8",
                "nine":"9"}

character_names = "space | amp | star | slosh | bar | coal | dash | drip | dot | quote | chud | bang | hash | plus | flash | smote | ray | Shem | lang | rang | lace | race | lack | rack | lop | hype | Al | Braa | Chow | Doy | Eve | Fay | Goo | Hoe | Ice | Jaa | Koi | Lee | Mao | Noy | Oak | Poe | Quinn | Roy | Soy | Tao | Ugh | Vote | Wes | Ecks | Yaa | Zoo | zero | one | two | three | four | five | six | seven | eight | nine"

ordinal_map = {"second":2, "third":3, "fourth":4, "fifth":5, "sixth":6}

def find_nth(search_in, find_me, n):
    start = search_in.find(find_me)
    while start >= 0 and n > 1:
        start = search_in.find(find_me, start + len(find_me))
        n -= 1
    return start

class Example(CompoundRule):
    spec = "look [(second | third | fourth | fifth | sixth)] (<text> | " + character_names + ")"

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
            to_find = character_map[character_to_find]
        
        to_find = to_find.lower()
        searching_message = "Searching for " + ordinal_arg + ": "  if ordinal_arg else "Searching for: " 
        print searching_message + to_find 
        Key("end,s-home,c-c").execute()  # 
        line = utils.getSelectedText().lower()
        line_index = -1
        if ordinal_arg:
            line_index = find_nth(line, to_find, ordinal_map[ordinal_arg])
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
