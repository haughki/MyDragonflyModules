from unittest import TestCase
from hawk import utils




class TestUtils(TestCase):
    def test_touch(self):
        utils.touch("D:\\temp\\temp.txt")

