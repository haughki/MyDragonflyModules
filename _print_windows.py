from dragonfly import CompoundRule, Grammar, Window


class PrintWindowsRule(CompoundRule):
    spec = "print Windows"  # Spoken form of command.

    def _process_recognition(self, node, extras):  # Callback when command is spoken.
        print node.words()

        for window in Window.get_all_windows():
            if window.is_visible:
                print '{:75} : {}'.format(unicode(window.executable.lower()), unicode(window.title.lower()))


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
