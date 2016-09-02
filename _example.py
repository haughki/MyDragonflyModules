# import sys
# sys.path.append('pycharm-debug.egg')
# import pydevd
# pydevd.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)



from dragonfly import *

from supporting import utils

character_names = "space | amp | star | slosh | bar | coal | dash | drip | dot | quote | chud | bang | hash | plus | flash | smote | ray | Shem | lang | rang | lace | race | lack | rack | lop | hype | Al | Braa | Chow | Doy | Eve | Fay | Goo | Hoe | Ice | Jaa | Koi | Lee | Mao | Noy | Oak | Poe | Quinn | Roy | Soy | Tao | Ugh | Vote | Wes | Ecks | Yaa | Zoo | zero | one | two | three | four | five | six | seven | eight | nine"

class Example(CompoundRule):
    spec = "search line (<text> | " + character_names + ")"

    extras = [Dictation("text")]
    defaults = {"text":""}

    def _process_recognition(self, node, extras):
        to_find = str(extras["text"])
        if to_find == "":
            print "nothing"
            to_find = node.words()[-1]
        print "searching for: " + to_find 
        Key("end,s-home,c-c").execute()
        line = utils.getSelectedText()
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
