from dragonfly import *

from languages import python_rule, java_rule

the_python_rule = python_rule.PythonRule()
the_java_rule = java_rule.JavaRule()

supported_languages = {"python": the_python_rule, "java": the_java_rule}
for supported in supported_languages:
    if supported != "python":
        supported_languages[supported].disable()

def disableAll():
    for lang in supported_languages:
        if supported_languages[lang].enabled:
            supported_languages[lang].disable()

class SetLanguageRule(CompoundRule):
    spec = "[set] language (python | java)"

    def _process_recognition(self, node, extras):
        lang_to_activate = node.words()[-1]
        print "activating " + lang_to_activate

        disableAll()

        if not supported_languages[lang_to_activate].enabled:
            supported_languages[lang_to_activate].enable()

context = AppContext(executable="idea64")
switcher_grammar = Grammar("switcher grammar", context=context)
switcher_grammar.add_rule(SetLanguageRule())
switcher_grammar.add_rule(the_python_rule)
switcher_grammar.add_rule(the_java_rule)
switcher_grammar.load()

def unload():
    global switcher_grammar
    if switcher_grammar:
        print "unloading " + __name__ + "..."
        switcher_grammar.unload()
    switcher_grammar = None
