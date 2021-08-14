import json


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    @property
    def ok(self):
        return self.status_code in [200, 201, 202]

    @property
    def content(self):
        return b"bytes"

    @property
    def text(self):
        return json.dumps(self.json_data)
