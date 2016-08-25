from unittest import TestCase
import inspect
from supporting.method_builder import method_builder

class TestClass(object):
    def __init__(self, name):
        self._name = name

    def noParameters(self):
        pass
    
    def oneParameter(self, name):
        pass

    def oneParameterWithDefault(self, my_default=None):
        pass

    def twoParameters(self, parameter1, parameter2):
        pass

    def twoParametersOneDefault(self, parameter1, my_default=None):
        pass


class TestMethodBuilder(TestCase):
    def test_method_builder_no_self(self):
        method_list = inspect.getmembers(TestClass, inspect.ismethod)
        codelist = method_builder(method_list, "object_to_call", False)
        codelist.sort()
        # print codelist
        
        self.assertEquals(codelist[0], 'def noParameters(): object_to_call.noParameters()')
        self.assertEquals(codelist[1], 'def oneParameter(name): object_to_call.oneParameter(name)')
        self.assertEquals(codelist[2], 'def oneParameterWithDefault(my_default=None): object_to_call.oneParameterWithDefault(my_default)')
        self.assertEquals(codelist[3], 'def twoParameters(parameter1, parameter2): object_to_call.twoParameters(parameter1, parameter2)')
        self.assertEquals(codelist[4], 'def twoParametersOneDefault(parameter1, my_default=None): object_to_call.twoParametersOneDefault(parameter1, my_default)')

    def test_method_builder_with_self(self):
        method_list = inspect.getmembers(TestClass, inspect.ismethod)
        codelist = method_builder(method_list, "object_to_call", True)
        codelist.sort()
        print codelist

        self.assertEquals(codelist[0], 'def noParameters(self): object_to_call.noParameters()')
        self.assertEquals(codelist[1], 'def oneParameter(self, name): object_to_call.oneParameter(name)')
        self.assertEquals(codelist[2], 'def oneParameterWithDefault(self, my_default=None): object_to_call.oneParameterWithDefault(my_default)')
        self.assertEquals(codelist[3], 'def twoParameters(self, parameter1, parameter2): object_to_call.twoParameters(parameter1, parameter2)')
        self.assertEquals(codelist[4], 'def twoParametersOneDefault(self, parameter1, my_default=None): object_to_call.twoParametersOneDefault(parameter1, my_default)')
