from json.decoder import JSONDecodeError

import requests

from heron import _base_url, error


class Envelope:
    def __init__(self, single, many):
        self.single = single
        self.many = many


class BaseResource:
    _envelope = None
    _path = None
    _prefix = ""

    def __init__(self, **kwargs):
        self.heron_id = kwargs.get("heron_id")

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.heron_id}>"

    @classmethod
    def do_request(cls, method, path=None, json=None, retry=False, **params):
        from heron import basic_auth_password, basic_auth_username

        if not path:
            path = cls._path
        kwargs = {"params": params} if params else {}

        req = getattr(requests, method)
        res = req(
            f"{_base_url}/{path}",
            headers={"Content-Type": "application/json"},
            json=json,
            auth=requests.auth.HTTPBasicAuth(
                basic_auth_username or "",
                basic_auth_password or "",
            ),
            **kwargs,
        )
        if res.ok:
            try:
                payload = res.json()[cls._envelope.single]
            except KeyError:
                pass
            else:
                return cls(**payload)
            try:
                payloads = res.json()[cls._envelope.many]
            except KeyError:
                pass
            else:
                return [cls(**payload) for payload in payloads]
            return None

        try:
            error_json = res.json()
        except JSONDecodeError:
            error_json = {"description": "Something went wrong"}

        if res.status_code == 422:
            e = error.HeronValidationError(error_json["description"])
            e.code = res.status_code
            e.json = error_json
            raise e

        if not str(res.status_code).startswith("5") or not retry:
            try:
                error_msg = error_json["description"] or error_json["name"]
            except KeyError:
                error_msg = "Something went wrong"
            e = error.HeronError(error_msg)
            e.code = res.status_code
            e.json = error_json
            raise e

        return cls.do_request(method, path=path, json=json, retry=False, **params)

    @classmethod
    def create(cls, path=None, **body):
        json = {cls._envelope.single: body}
        return cls.do_request("post", path=path, json=json, retry=True)

    @classmethod
    def create_many(cls, bodies, path=None):
        json = {cls._envelope.many: bodies}
        return cls.do_request("post", path=path, json=json, retry=True)

    @classmethod
    def update(cls, path=None, **body):
        json = {cls._envelope.single: body}
        return cls.do_request("put", path=path, json=json)

    @classmethod
    def list(cls, path=None, **params):
        return cls.do_request("get", path=path, retry=True, **params)

    @classmethod
    def get(cls, resource_id):
        if not isinstance(resource_id, str):
            raise ValueError(f"{cls._envelope.single}_id must be a string")
        if not resource_id.startswith(cls._prefix):
            raise ValueError(
                f"invalid {cls._envelope.single}_id, must start with '{cls._prefix}'"
            )
        return cls.do_request("get", path=f"{cls._path}/{resource_id}", retry=False)
