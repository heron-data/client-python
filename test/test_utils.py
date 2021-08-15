import unittest

from heron import utils


class TestUtils(unittest.TestCase):
    def test_to_dollars(self):
        self.assertEqual(utils.to_dollars(None), None)
        self.assertEqual(utils.to_dollars("1000"), 10.00)
        self.assertEqual(utils.to_dollars(1000), 10.00)
        self.assertEqual(utils.to_dollars(10.00), 10.00)
        with self.assertRaises(ValueError):
            utils.to_dollars("1000.00")
        with self.assertRaises(ValueError):
            utils.to_dollars("foo")
