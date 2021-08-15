import unittest
from unittest.mock import ANY, patch

from heron import Category, EndUser, Merchant, Transaction, error

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
            mock_post.assert_called_once_with(
                ANY, headers=ANY, json=self.request_payload, auth=ANY
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

    def test_create_with_end_user_id(self):
        with patch("requests.post") as mock_post:
            mock_post.return_value = MockResponse(self.response_payload, 200)

            transaction = Transaction.create(
                **self.request_payload["transactions"][0],
                end_user=self.end_user.end_user_id
            )

            self.assertIsInstance(transaction, Transaction)
            self.assertIsInstance(transaction.categories[0], Category)
            self.assertIsInstance(transaction.merchant, Merchant)
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

    def test_with_end_user_object_no_end_user_id(self):
        with patch("requests.post") as mock_post:
            mock_post.return_value = MockResponse(self.response_payload, 200)

            self.end_user.end_user_id = None  # not valid

            with self.assertRaises(ValueError):
                Transaction.create(
                    **self.request_payload["transactions"][0], end_user=self.end_user
                )

            mock_post.assert_not_called()


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
                mock_post.assert_called_once_with(
                    ANY, headers=ANY, json=self.request_payload, auth=ANY
                )

    def test_invalid_args(self):
        with patch("requests.post") as mock_post:
            mock_post.return_value = MockResponse(self.response_payload, 200)

            with self.assertRaises(ValueError):
                Transaction.create_many({})  # not a list
            with self.assertRaises(ValueError):
                Transaction.create_many([])  # empty list
            with self.assertRaises(ValueError):
                Transaction.create_many([123])  # not a dict
            with self.assertRaises(ValueError):
                Transaction.create_many([{"amount": 12.2}])  # no description
            with self.assertRaises(ValueError):
                Transaction.create_many(
                    [{"amount": 12.2, "description": "foo"}],
                    end_user=1,
                )  # bad end_user

            mock_post.assert_not_called()


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

            transactions = Transaction.list(end_user_id="1")

            for transaction in transactions:
                self.assertIsInstance(transaction, Transaction)
                self.assertIsInstance(transaction.categories[0], Category)
                self.assertIsInstance(transaction.merchant, Merchant)
                self.assertIsInstance(transaction.payment_processor, Merchant)
                mock_get.assert_called_once_with(
                    ANY, headers=ANY, json=None, auth=ANY, params={"end_user_id": "1"}
                )

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


class TestFeedback(unittest.TestCase):
    def setUp(self):
        self.transaction_id = "txn_123"
        self.transaction = Transaction(heron_id=self.transaction_id)
        self.merchant_name = "Foo"
        self.merchant_id = "mrc_123"
        self.merchant = Merchant(heron_id=self.merchant_id)
        self.category_label = "Bar"
        self.category_id = "ctg_123"
        self.category = Category(heron_id=self.category_id)

    def test_category_label_feedback(self):
        with patch("requests.put") as mock_put:
            mock_put.return_value = MockResponse({}, 200)

            Transaction.feedback(
                transaction=self.transaction_id,
                category=self.category_label,
            )

            mock_put.assert_called_once_with(
                ANY,
                headers=ANY,
                json={"transaction": {"category": {"label": self.category_label}}},
                auth=ANY,
            )

    def test_category_id_feedback(self):
        with patch("requests.put") as mock_put:
            mock_put.return_value = MockResponse({}, 200)

            Transaction.feedback(
                transaction=self.transaction_id,
                category=self.category_id,
            )

            mock_put.assert_called_once_with(
                ANY,
                headers=ANY,
                json={"transaction": {"category": {"heron_id": self.category_id}}},
                auth=ANY,
            )

    def test_category_feedback(self):
        with patch("requests.put") as mock_put:
            mock_put.return_value = MockResponse({}, 200)

            Transaction.feedback(
                transaction=self.transaction_id,
                category=self.category,
            )

            mock_put.assert_called_once_with(
                ANY,
                headers=ANY,
                json={"transaction": {"category": {"heron_id": self.category_id}}},
                auth=ANY,
            )

    def test_merchant_name_feedback(self):
        with patch("requests.put") as mock_put:
            mock_put.return_value = MockResponse({}, 200)

            Transaction.feedback(
                transaction=self.transaction_id,
                merchant=self.merchant_name,
            )

            mock_put.assert_called_once_with(
                ANY,
                headers=ANY,
                json={"transaction": {"merchant": {"name": self.merchant_name}}},
                auth=ANY,
            )

    def test_merchant_id_feedback(self):
        with patch("requests.put") as mock_put:
            mock_put.return_value = MockResponse({}, 200)

            Transaction.feedback(
                transaction=self.transaction_id,
                merchant=self.merchant_id,
            )

            mock_put.assert_called_once_with(
                ANY,
                headers=ANY,
                json={"transaction": {"merchant": {"heron_id": self.merchant_id}}},
                auth=ANY,
            )

    def test_merchant_feedback(self):
        with patch("requests.put") as mock_put:
            mock_put.return_value = MockResponse({}, 200)

            Transaction.feedback(
                transaction=self.transaction_id,
                merchant=self.merchant,
            )

            mock_put.assert_called_once_with(
                ANY,
                headers=ANY,
                json={
                    "transaction": {"merchant": {"heron_id": self.merchant.heron_id}}
                },
                auth=ANY,
            )

    def test_merchant_and_category_feedback(self):
        with patch("requests.put") as mock_put:
            mock_put.return_value = MockResponse({}, 200)

            Transaction.feedback(
                transaction=self.transaction_id,
                merchant=self.merchant,
                category=self.category,
            )

            mock_put.assert_called_once_with(
                ANY,
                headers=ANY,
                json={
                    "transaction": {
                        "merchant": {"heron_id": self.merchant_id},
                        "category": {"heron_id": self.category_id},
                    }
                },
                auth=ANY,
            )

    def test_no_feedback(self):
        with patch("requests.put") as mock_put:
            mock_put.return_value = MockResponse({}, 200)

            with self.assertRaises(ValueError):
                Transaction.feedback(transaction=self.transaction_id)

            mock_put.assert_not_called()

    def test_invalid_heron_ids(self):
        with patch("requests.put") as mock_put:
            mock_put.return_value = MockResponse({}, 200)

            with self.assertRaises(ValueError):
                Transaction.feedback(transaction="not_an_id")

            mock_put.assert_not_called()

    def test_invalid_kwargs(self):
        with patch("requests.put") as mock_put:
            mock_put.return_value = MockResponse({}, 200)

            with self.assertRaises(ValueError):
                Transaction.feedback(
                    transaction=self.transaction,
                    merchant=123,
                )
            with self.assertRaises(ValueError):
                Transaction.feedback(
                    transaction=self.transaction_id,
                    category=123,
                )
            with self.assertRaises(ValueError):
                Transaction.feedback(
                    transaction=123,
                    category=self.category_id,
                )

            mock_put.assert_not_called()
