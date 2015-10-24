import inspect

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