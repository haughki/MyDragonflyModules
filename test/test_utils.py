from unittest import TestCase
from supporting import utils




class TestUtils(TestCase):
    def test_touch(self):
        utils.touch("D:\\temp\\temp.txt")

