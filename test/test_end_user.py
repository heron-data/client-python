import unittest
from unittest.mock import ANY, patch

from heron import EndUser

from .mocks import MockResponse


class TestRepr(unittest.TestCase):
    def test_repr(self):
        e = EndUser(heron_id="eus_1", name="foo")
        self.assertEqual(str(e), "<EndUser eus_1: foo>")


class TestEndUser(unittest.TestCase):
    def setUp(self):
        self.end_user_dict = {
            "name": "Foo",
            "end_user_id": "foo-123",
        }
        self.enrichments = {
            "status": "new",
        }
        self.request_payload = {"end_user": {**self.end_user_dict, **self.enrichments}}
        self.response_payload = self.request_payload

    def test_create(self):
        with patch("requests.post") as mock_post:
            mock_post.return_value = MockResponse(self.response_payload, 200)

            end_user = EndUser.create(**self.end_user_dict)

            self.assertIsInstance(end_user, EndUser)
            mock_post.assert_called_once_with(
                ANY, headers=ANY, json=self.request_payload, auth=ANY
            )

    def test_update(self):
        with patch("requests.put") as mock_put:
            mock_put.return_value = MockResponse(self.response_payload, 200)
            new_status = "ready"

            end_user = EndUser.update(**self.end_user_dict, status=new_status)

            self.assertIsInstance(end_user, EndUser)
            mock_put.assert_called_once_with(
                ANY,
                headers=ANY,
                json={
                    "end_user": {
                        **self.end_user_dict,
                        "status": new_status,
                    },
                },
                auth=ANY,
            )

    def test_list(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value = MockResponse({"end_users": []}, 200)
            params = {"page": 1, "limit": 100}

            EndUser.list(**params)

            mock_get.assert_called_once_with(
                ANY, headers=ANY, json=None, auth=ANY, params=params
            )
