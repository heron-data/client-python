import unittest
from unittest.mock import ANY, patch

from heron import Merchant

from .mocks import MockResponse


class TestRepr(unittest.TestCase):
    def test_repr(self):
        m = Merchant(heron_id="mrc_1", name="foo")
        self.assertEqual(str(m), "<Merchant mrc_1: foo>")


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.merchant_dict = {
            "heron_id": "mrc_123",
            "name": "Spotify",
            "url": "foo.com",
            "logo_url": "logo.foo.com",
            "icon_url": "icon.foo.com",
        }
        self.response_payload = {"merchants": [self.merchant_dict] * 3}

    def test_search(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value = MockResponse(self.response_payload, 200)

            merchants = Merchant.search(name="Spot")

            for merchant in merchants:
                self.assertIsInstance(merchant, Merchant)
                self.assertEqual(merchant.heron_id, self.merchant_dict["heron_id"])
                mock_get.assert_called_once_with(
                    ANY, headers=ANY, json=None, auth=ANY, params={"name": "Spot"}
                )


class TestGet(unittest.TestCase):
    def setUp(self):
        self.merchant_dict = {
            "heron_id": "mrc_123",
            "name": "Spotify",
            "url": "foo.com",
            "logo_url": "logo.foo.com",
            "icon_url": "icon.foo.com",
        }
        self.response_payload = {"merchant": self.merchant_dict}

    def test_get(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value = MockResponse(self.response_payload, 200)

            merchant = Merchant.get(self.merchant_dict["heron_id"])

            self.assertIsInstance(merchant, Merchant)
            self.assertEqual(merchant.heron_id, self.merchant_dict["heron_id"])
            mock_get.assert_called_once_with(ANY, headers=ANY, json=None, auth=ANY)

    def test_invalid_heron_id(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value = MockResponse(self.response_payload, 200)

            with self.assertRaises(ValueError):
                Merchant.get("merchaaant")
            with self.assertRaises(ValueError):
                Merchant.get(123)

            mock_get.assert_not_called()


class TestCreate(unittest.TestCase):
    def test_not_implemented(self):
        with patch("requests.post") as mock_request:
            mock_request.return_value = MockResponse({}, 200)

            with self.assertRaises(NotImplementedError):
                Merchant.create()

            mock_request.assert_not_called()


class TestCreateMany(unittest.TestCase):
    def test_not_implemented(self):
        with patch("requests.post") as mock_request:
            mock_request.return_value = MockResponse({}, 200)

            with self.assertRaises(NotImplementedError):
                Merchant.create_many()

            mock_request.assert_not_called()


class TestUpdate(unittest.TestCase):
    def test_not_implemented(self):
        with patch("requests.put") as mock_request:
            mock_request.return_value = MockResponse({}, 200)

            with self.assertRaises(NotImplementedError):
                Merchant.update(label="1")

            mock_request.assert_not_called()


class TestList(unittest.TestCase):
    def test_not_implemented(self):
        with patch("requests.get") as mock_request:
            mock_request.return_value = MockResponse({}, 200)

            with self.assertRaises(NotImplementedError):
                Merchant.list()

            mock_request.assert_not_called()
