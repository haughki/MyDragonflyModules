try:
    import pkg_resources

    pkg_resources.require("dragonfly >= 0.6.5beta1.dev-r99")
except ImportError:
    pass

from dragonfly import *

# from dragonfly.actions.action_mimic import Mimic
# from dragonfly.all import Grammar
# from dragonfly.grammar.rule_mapping import MappingRule


class FocusMimics(MappingRule):
    """ This mimics the "switch to" command from DNS to use the Dragonfly "focus" command syntax.
    The main definitions of the Dragonfly "focus" command are in _window_control.py.
    """
    mapping = {
        "focus chrome": Mimic("switch", "to", "Google Chrome"),
        "focus note": Mimic("switch", "to", "notepad++"),
        "focus word": Mimic("switch", "to", "Microsoft Word"),
        "focus evernote": Mimic("switch", "to", "evernote"),
        "focus fire": Mimic("switch", "to", "Firefox"),
        #"focus idea": Mimic("switch", "to", "IntelliJ IDEA 14.1.5"),
        "focus plore": Mimic("switch", "to", "Windows Explorer"),
    }


# Create a grammar which contains and loads the command rule.
grammar = Grammar("my windows grammar")
grammar.add_rule(FocusMimics())

grammar.load()


def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
