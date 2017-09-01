import gc
import inspect
import os

from dragonfly import Key
from dragonfly.windows.clipboard import Clipboard

__author__ = 'parkerh'


def unloadHelper(grammar, name):
    if grammar:
        print "unloading " + name + "..."
        grammar.unload()
    return None



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
    
    # print "original before copy: " + original.get_text()
    
    Key("c-c/5").execute()
    # note that trying to re-use this clipboard object after it's been
    # modified has caused me issues in the past -- seems to hold onto old values...
    just_copied = Clipboard()
    just_copied.copy_from_system()
    
    # print "original after copy: " + original.get_text()
    # print "just copied before original copy back: " + just_copied.get_text()
    
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

def buildNumber(w, x=None, y=None, z=None):
    """ Each input variable is a number 0...9, so that w=1, x=4, y=2 would produce 142 """
    number = str(w)
    if x is not None:
        number += str(x)
    if y is not None:
        number += str(y)
    if z is not None:
        number += str(z)
    return number

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