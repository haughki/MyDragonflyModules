from dragonfly import Function, MappingRule, Text, Dictation, Config, Section, Item, Key

config = Config("format functions")
config.cmd = Section("Command section")
config.cmd.map = Item(
    {},
    namespace={
        "Key": Key,
        "Text": Text,
    }
)
namespace = config.load()


#---------------------------------------------------------------------------
# Here we prepare the list of formatting functions from the config file.

# Retrieve text-formatting functions from this module's config file. Each of these functions must have a name that starts with "format_".
format_functions = {}
if namespace:
    for name, function in namespace.items():
        if name.startswith("format_") and callable(function):
            spoken_form = function.__doc__.strip()

            # We wrap generation of the Function action in a function so that its *function* variable will be local.  Otherwise it
            #  would change during the next iteration of the namespace loop.
            def wrap_function(function):
                def _function(dictation):
                    formatted_text = function(dictation)
                    Text(formatted_text).execute()

                return Function(_function)

            action = wrap_function(function)
            format_functions[spoken_form] = action


# Here we define the text formatting rule. The contents of this rule were built up from the "format_*"
#  functions in this module's config file.
class FormatRule(MappingRule):
    mapping = format_functions
    extras = [Dictation("dictation")]
