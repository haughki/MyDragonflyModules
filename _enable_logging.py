import logging
from dragonfly import log, CompoundRule, Grammar

log.setup_log()
# log.setup_tracing()

class LoggingRule(CompoundRule):
    spec = "is logging enabled"                  # Spoken form of command.

    def _process_recognition(self, node, extras):   # Callback when command is spoken.
        print 'Yes, looging should be enabled.'

        testlog = logging.getLogger("dfly.test")
        testlog.debug("Test the dragonfly test log.")

        engine_log = logging.getLogger("engine")
        engine_log.info("The file log should see this, but not stdout.")
        engine_log.warning("Both file and stdout logs should see this.")

#Create a grammar which contains and loads the command rule.
logging_rule = LoggingRule()
grammar = Grammar("example grammar")
grammar.add_rule(logging_rule)
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None