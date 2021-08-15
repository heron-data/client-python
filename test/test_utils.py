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

    def test_to_iso_format(self):
        self.assertEqual(
            utils.to_iso_format("2017-01-29T00:00:00"), "2017-01-29T00:00:00"
        )
        self.assertEqual(utils.to_iso_format("1611878400"), "2021-01-29T00:00:00")
        self.assertEqual(utils.to_iso_format(1611878400), "2021-01-29T00:00:00")
        with self.assertRaises(ValueError):
            utils.to_iso_format("1000.00")
        with self.assertRaises(ValueError):
            utils.to_iso_format(None)
