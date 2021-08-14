import unittest
from unittest.mock import ANY, patch

from heron import error
from heron.resources import Category, EndUser, Merchant, Transaction

from .mocks import MockResponse


class TestCreate(unittest.TestCase):
    def setUp(self):
        self.transaction_dict = {
            "amount": 11.11,
            "description": "foo bar 123",
        }
        self.enrichments = {
            "description_clean": "foo bar",
            "categories": [
                {
                    "heron_id": "ctg_123",
                    "annotator": "heuristics",
                    "label": "Expenses",
                    "confidence": 0.9,
                },
            ],
            "merchant": {
                "heron_id": "mrc_123",
                "name": "Bar",
                "url": "https://www.bar.com/",
                "logo_url": "https://logos.herondata.io/123",
                "icon_url": "https://icons.herondata.io/123",
            },
            "payment_processor": {
                "heron_id": "mrc_456",
                "name": "Foo",
                "url": "https://www.foo.com/",
            },
        }
        self.request_payload = {"transactions": [self.transaction_dict]}
        self.response_payload = {
            "transactions": [{**self.transaction_dict, **self.enrichments}]
        }
        self.end_user = EndUser(end_user_id="bar")

    def test_create(self):
        with patch("requests.post") as mock_post:
            mock_post.return_value = MockResponse(self.response_payload, 200)

            transaction = Transaction.create(**self.request_payload["transactions"][0])

            self.assertIsInstance(transaction, Transaction)
            self.assertIsInstance(transaction.categories[0], Category)
            self.assertIsInstance(transaction.merchant, Merchant)
            self.assertIsInstance(transaction.payment_processor, Merchant)
            self.assertIsNone(
                mock_post.assert_called_once_with(
                    ANY, headers=ANY, json=self.request_payload, auth=ANY
                )
            )

    def test_create_with_end_user(self):
        with patch("requests.post") as mock_post:
            mock_post.return_value = MockResponse(self.response_payload, 200)

            transaction = Transaction.create(
                **self.request_payload["transactions"][0], end_user=self.end_user
            )

            self.assertIsInstance(transaction, Transaction)
            self.assertIsInstance(transaction.categories[0], Category)
            self.assertIsInstance(transaction.merchant, Merchant)
            self.assertIsNone(
                mock_post.assert_called_once_with(
                    ANY,
                    headers=ANY,
                    json={
                        "transactions": [
                            {
                                **self.request_payload["transactions"][0],
                                **{
                                    "end_user_id": self.end_user.end_user_id,
                                },
                            }
                        ]
                    },
                    auth=ANY,
                )
            )


class TestCreateMany(unittest.TestCase):
    def setUp(self):
        self.transaction_dict = {
            "amount": 11.11,
            "description": "foo bar 123",
        }
        self.enrichments = {
            "description_clean": "foo bar",
            "categories": [
                {
                    "heron_id": "ctg_123",
                    "annotator": "heuristics",
                    "label": "Expenses",
                    "confidence": 0.9,
                },
            ],
            "merchant": {
                "heron_id": "mrc_123",
                "name": "Bar",
                "url": "https://www.bar.com/",
                "logo_url": "https://logos.herondata.io/123",
                "icon_url": "https://icons.herondata.io/123",
            },
            "payment_processor": {
                "heron_id": "mrc_456",
                "name": "Foo",
                "url": "https://www.foo.com/",
            },
        }
        self.request_payload = {"transactions": [self.transaction_dict] * 3}
        self.response_payload = {
            "transactions": [{**self.transaction_dict, **self.enrichments}] * 3
        }

    def test_create_many(self):
        with patch("requests.post") as mock_post:
            mock_post.return_value = MockResponse(self.response_payload, 200)

            transactions = Transaction.create_many(self.request_payload["transactions"])

            for transaction in transactions:
                self.assertIsInstance(transaction, Transaction)
                self.assertIsInstance(transaction.categories[0], Category)
                self.assertIsInstance(transaction.merchant, Merchant)
                self.assertIsInstance(transaction.payment_processor, Merchant)
                self.assertIsNone(
                    mock_post.assert_called_once_with(
                        ANY, headers=ANY, json=self.request_payload, auth=ANY
                    )
                )


class TestList(unittest.TestCase):
    def setUp(self):
        self.transaction_dict = {
            "amount": 11.11,
            "description": "foo bar 123",
        }
        self.enrichments = {
            "description_clean": "foo bar",
            "categories": [
                {
                    "heron_id": "ctg_123",
                    "annotator": "heuristics",
                    "label": "Expenses",
                    "confidence": 0.9,
                },
            ],
            "merchant": {
                "heron_id": "mrc_123",
                "name": "Bar",
                "url": "https://www.bar.com/",
                "logo_url": "https://logos.herondata.io/123",
                "icon_url": "https://icons.herondata.io/123",
            },
            "payment_processor": {
                "heron_id": "mrc_456",
                "name": "Foo",
                "url": "https://www.foo.com/",
            },
        }
        self.response_payload = {
            "transactions": [{**self.transaction_dict, **self.enrichments}] * 3
        }
        self.validation_error_payload = {
            "code": 422,
            "name": "Unprocessable Entity",
            "description": {},
        }

    def test_list(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value = MockResponse(self.response_payload, 200)

            transactions = Transaction.list()

            for transaction in transactions:
                self.assertIsInstance(transaction, Transaction)
                self.assertIsInstance(transaction.categories[0], Category)
                self.assertIsInstance(transaction.merchant, Merchant)
                self.assertIsInstance(transaction.payment_processor, Merchant)
                mock_get.assert_called_once_with(ANY, headers=ANY, json=None, auth=ANY)

    def test_validation_error(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value = MockResponse(self.validation_error_payload, 422)

            with self.assertRaises(error.HeronValidationError):
                transactions = Transaction.list()
                self.assertIsNone(transactions)
                mock_get.assert_called_once_with(ANY, headers=ANY, json=None, auth=ANY)

    def test_internal_server_error(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value = MockResponse({}, 500)

            with self.assertRaises(error.HeronError):
                transactions = Transaction.list()
                self.assertIsNone(transactions)
                mock_get.assert_called_once_with(ANY, headers=ANY, json=None, auth=ANY)
