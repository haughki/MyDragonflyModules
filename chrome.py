from dragonfly import (Grammar, AppContext, MappingRule, Integer, Key, Text, Mimic, Dictation, Function, CompoundRule,
                       Pause)

class GlobalChromeMappings(MappingRule):
    mapping = {
        'new (thing | tab)': Key('c-t'),
        'reopen tab': Key('cs-t'),
        '(next | nex) tab [<n>]': Key('c-pgdown:%(n)d'),
        '(previous | preev) tab [<n>]': Key('c-pgup:%(n)d'),
        'show tab <tab>': Key('c-%(tab)d'),
        '(first | firs) tab': Key('c-1'),
        '(last | lass | las ) tab': Key('c-9'),
        'go back': Key('a-left'),
        'go forward': Key('a-right'),
        'address [bar]': Key('a-d'),
        'refresh page': Key('f5'),
        'find <text>': Key("c-g/25") + Text("%(text)s"),
        'find next': Key('enter'),
        'find (prev | previous)': Key('s-enter'),
        'bookmark page': Key('c-d'),
        'open': Key('f'),                         # vimium
        'tabs': Key('s-f'),                       # vimium
        '(go | choose) <number>': Text('%(number)d'),        # vimium
        '(duplicate | dupe) tab': Key('y/25,t'),  # vimium
    }
    extras=[
        Integer('n', 1, 50),
        Integer('tab', 1, 8),
        Integer('number', 1, 9999),
        Dictation("text"),
    ]
    defaults = {
        "n": 1,
    }

class GmailMappings(MappingRule):
    mapping = {
        "compose": Key("c"),
        'next mail [<n>]': Key('j:%(n)d'),
        '(previous | preev) mail [<n>]': Key('k:%(n)d'),
        '[go to] inbox': Key('g,i'),
        "(delete | trash)": Key("hash"),
        "line trash": Key("x/5,hash"),
        "send it": Key("c-enter"),
        'reply': Key('r'),
        'reply all': Key('a'),
        'forward': Key('f'),
        'select': Key('x'),
        "move": Key('v'),
        "[move to] receipts": Key('x,v/20') + Text("receipts") + Key('enter'),
        "send archive": Mimic("click", "send", "and", "archive"),
    }

    extras = [
        Dictation("text"),
        Integer('n', 1, 50),
    ]

    defaults = {
        "n": 1,
    }

class OpenGmailLineRule(CompoundRule):
    """ Mimics the Dragon builtin command ("click <subject>") to open a Gmail line item.
    Always "chooses 2" to bypass that step.
    """
    spec = "take <text>"
    extras = [
        Dictation("text"),
    ]

    def _process_recognition(self, node, extras):
        dictation = str(extras["text"]).split()  # this is the target email subject
        dictation.insert(0, "click")  # this adds the "click" command for Dragon

        Mimic(*dictation).execute()  # expand the list to var args

        #Pause("10").execute()  # doesn't seem to need this...

        Mimic("choose", "2").execute()


#gmail_context = AppContext(executable='chrome', title='Gmail')

context = AppContext(executable='chrome')
grammar = Grammar('Google Chrome', context=context)
grammar.add_rule(GlobalChromeMappings())
grammar.add_rule(GmailMappings())
grammar.add_rule(OpenGmailLineRule())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
