import inspect, os
from dragonfly.windows.clipboard import Clipboard
from dragonfly import Key

__author__ = 'parkerh'


def getClassFields(aClass):
    classFields = []
    objectMembers = dir(type('dummy', (object,), {}))
    for classMember in inspect.getmembers(aClass):
        if not inspect.ismethod(classMember[1]):
            isUniqueToClass = True
            for objectMember in objectMembers:
                if classMember[0] == objectMember:
                    isUniqueToClass = False
            if isUniqueToClass:
                classFields.append(classMember[0])

    return classFields


def windowIsValid(window):
    if not window.is_visible:
        return False
    if not window.executable:
        return False
    if not window.title:
        return False
    if window.title == "Start":
        return False
    if window.title == "Program Manager":
        return False
    return True


def getSelectedText():
    """ Get the currently selected text by copying it to the clipboard and pulling it from there.
    Preserve the original clipboard state. """
    original = Clipboard(from_system=True)
    
    Key("c-c").execute()
    # note that trying to re-use this clipboard object after it's been
    # modified has caused me issues in the past -- seems to hold onto old values...
    just_copied = Clipboard()
    just_copied.copy_from_system()

    original.copy_to_system()  # restore the state of the clipboard

    return just_copied.get_text()


def find_nth(search_in, find_me, n):
    start = search_in.find(find_me)
    while start >= 0 and n > 1:
        start = search_in.find(find_me, start + len(find_me))
        n -= 1
    return start


def touch(fname, times=None):
    fhandle = open(fname, 'a')
    try:
        os.utime(fname, times)
    finally:
        fhandle.close()

def toggleMicrophone():
    Key("npadd/10,npadd").execute()


import gc

def objects_by_id(id_):
    for obj in gc.get_objects():
        if id(obj) == id_:
            return obj
    return None

def text_to_case(make_me, format_me):
    if make_me == "pascal":
        return pascal(format_me)
    elif make_me == "camel":
        return camel(format_me)
    elif make_me == "snake":
        return snake(format_me)
    return ""

def snake(text):
    # some_words
    words = [word.lower() for word in text.split(" ")]
    return "_".join(words)

def snake_function(text):
    # Format: some_words()
    return snake(text) + "()"

def upper_snake(text):
    # Format: SOME_WORDS
    words = [word.upper() for word in text.split(" ")]
    return "_".join(words)

def one_word(text):
    # Format: somewords
    words = [word.lower() for word in text.split(" ")]
    return "".join(words)

def upper_one_word(text):
    # Format: SOMEWORDS
    words = [word.upper() for word in text.split(" ")]
    return "".join(words)

def pascal(text):
    # Format: SomeWords
    words = [word.capitalize() for word in text.split(" ")]
    return "".join(words)

def pascal_function(text):
    # Format: SomeWords()
    return pascal(text) + "()"

def camel(text):
    # Format: someWords
    words = text.split(" ")
    return words[0] + "".join(w.capitalize() for w in words[1:])

def camel_function(text):
    # Format: someWords()
    return camel(text) + "()"