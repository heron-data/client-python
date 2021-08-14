import unittest
from unittest.mock import ANY, patch

from heron.resources import EndUser

from .mocks import MockResponse


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
        with patch("requests.put") as mock_post:
            mock_post.return_value = MockResponse(self.response_payload, 200)
            new_status = "ready"

            end_user = EndUser.update(**self.end_user_dict, status=new_status)

            self.assertIsInstance(end_user, EndUser)
            mock_post.assert_called_once_with(
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
