# import pydevd_pycharm
# pydevd_pycharm.settrace('localhost', port=8282, stdoutToServer=True, stderrToServer=True)


from dragonfly import CompoundRule, Grammar, Window
from supporting import utils

class PrintWindowsRule(CompoundRule):
    spec = "print [all] Windows"  # Spoken form of command.

    def _process_recognition(self, node, extras):  # Callback when command is spoken.
        windows = Window.get_all_windows()
        #windows.sort(key=lambda x: x.executable)
        for window in windows:
            if utils.windowIsValid(window):
                print "{:7} : {:75} : {}".format(window.handle, window.executable.encode("utf-8"), window.title.encode("utf-8"))


# window.executable.lower()
# window.title.lower()
# window.is_visible
# window.name
# window.classname


grammar = Grammar("print windows according to Python")
grammar.add_rule(PrintWindowsRule())

grammar.load()


def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
