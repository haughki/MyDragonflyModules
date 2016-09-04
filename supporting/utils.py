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
    Key("c-c").execute()
    # note that trying to re-use this clipboard object after it's been
    # modified has caused me issues in the past -- seems to hold onto old
    # values...
    clipboard = Clipboard()
    clipboard.copy_from_system()
    return clipboard.get_text()


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


import gc

def objects_by_id(id_):
    for obj in gc.get_objects():
        if id(obj) == id_:
            return obj
    return None