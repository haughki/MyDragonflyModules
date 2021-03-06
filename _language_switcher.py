from dragonfly import *

from languages import python_rule, java_rule, yaml_rule
from supporting import utils

the_python_rule = python_rule.PythonRule()
the_java_rule = java_rule.JavaRule()
the_yaml_rule = yaml_rule.YamlRule()

supported_languages = {"python": the_python_rule, "java": the_java_rule, "YAML": the_yaml_rule}
for supported in supported_languages:
    if supported != "python":
        supported_languages[supported].disable()

def disableAll():
    for lang in supported_languages:
        if supported_languages[lang].enabled:
            supported_languages[lang].disable()

class SetLanguageRule(CompoundRule):
    spec = "[set] language (python | java | YAML)"

    def _process_recognition(self, node, extras):
        lang_to_activate = node.words()[-1]
        print "activating " + lang_to_activate

        disableAll()

        if not supported_languages[lang_to_activate].enabled:
            supported_languages[lang_to_activate].enable()


idea_context = AppContext(executable="idea64")
code_context = AppContext(executable="code")
idea_or_code_context = idea_context | code_context
switcher_grammar = Grammar("switcher grammar", context=idea_or_code_context)
language_grammar = Grammar("language grammar", context=idea_or_code_context)
switcher_grammar.add_rule(SetLanguageRule())
language_grammar.add_rule(the_python_rule)
language_grammar.add_rule(the_java_rule)
language_grammar.add_rule(the_yaml_rule)
switcher_grammar.load()
language_grammar.load()

def unload():
    global switcher_grammar
    global language_grammar
    switcher_grammar = utils.unloadHelper(switcher_grammar, __name__ + ": switcher_grammar")
    language_grammar = utils.unloadHelper(language_grammar, __name__ + ": language_grammar")