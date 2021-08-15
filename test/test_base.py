import unittest

from heron.base import BaseResource


class TestRepr(unittest.TestCase):
    def test_repr(self):
        b = BaseResource(heron_id="res_1")
        self.assertEqual(str(b), "<BaseResource: res_1>")
