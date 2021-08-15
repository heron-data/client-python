import unittest
from unittest.mock import ANY, patch

from heron import Category

from .mocks import MockResponse


class TestRepr(unittest.TestCase):
    def test_repr(self):
        c = Category(heron_id="ctg_1", label="foo")
        self.assertEqual(str(c), "<Category ctg_1: foo>")


class TestList(unittest.TestCase):
    def setUp(self):
        self.category_dict = {
            "heron_id": "ctg_123",
            "label": "Other expenses",
            "confidence": 0.9,
        }
        self.response_payload = {"categories": [self.category_dict] * 3}

    def test_list(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value = MockResponse(self.response_payload, 200)

            categories = Category.list()

            for category in categories:
                self.assertIsInstance(category, Category)
                self.assertEqual(category.heron_id, self.category_dict["heron_id"])
                self.assertEqual(category.label, self.category_dict["label"])
                self.assertEqual(category.confidence, self.category_dict["confidence"])
                mock_get.assert_called_once_with(
                    ANY,
                    headers=ANY,
                    json=None,
                    auth=ANY,
                )


class TestCreate(unittest.TestCase):
    def test_not_implemented(self):
        with patch("requests.post") as mock_request:
            mock_request.return_value = MockResponse({}, 200)

            with self.assertRaises(NotImplementedError):
                Category.create()

            mock_request.assert_not_called()


class TestCreateMany(unittest.TestCase):
    def test_not_implemented(self):
        with patch("requests.post") as mock_request:
            mock_request.return_value = MockResponse({}, 200)

            with self.assertRaises(NotImplementedError):
                Category.create_many()

            mock_request.assert_not_called()


class TestUpdate(unittest.TestCase):
    def test_not_implemented(self):
        with patch("requests.put") as mock_request:
            mock_request.return_value = MockResponse({}, 200)

            with self.assertRaises(NotImplementedError):
                Category.update(label="1")

            mock_request.assert_not_called()
