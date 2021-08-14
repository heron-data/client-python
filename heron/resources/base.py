import requests


class Envelope:
    def __init__(self, single, many):
        self.single = single
        self.many = many


class BaseResource:
    _envelope = None
    _path = None

    @classmethod
    def do_request(cls, method, path=None, json=None, retry=False, **params):
        from heron import base_url, basic_auth_password, basic_auth_username, error

        if not path:
            path = cls._path

        req = getattr(requests, method)
        res = req(
            f"{base_url}/{path}",
            headers={"Content-Type": "application/json"},
            json=json,
            auth=requests.auth.HTTPBasicAuth(
                basic_auth_username or "",
                basic_auth_password or "",
            ),
            **params,
        )
        res_json = res.json()
        if res.ok:
            try:
                payload = res_json[cls._envelope.single]
            except KeyError:
                pass
            else:
                return cls(**payload)
            try:
                payloads = res_json[cls._envelope.many]
            except KeyError:
                pass
            else:
                return [cls(**payload) for payload in payloads]
            return None

        if res.status_code == 422:
            e = error.HeronValidationError(str(res.json()))
            e.code = res.status_code
            e.json = res_json
            raise e

        if not str(res.status_code).startswith("5") or not retry:
            try:
                e = error.HeronError(res.json()["name"])
            except KeyError:
                e = error.HeronError("Something went wrong")
            e.code = res.status_code
            e.json = res_json
            raise e

        return cls.do_request(method, path, json, retry=False, **params)

    @classmethod
    def create(cls, path=None, **kwargs):
        json = {cls._envelope.single: kwargs}
        return cls.do_request("post", path=path, json=json, retry=True)

    @classmethod
    def create_many(cls, ls, path=None):
        json = {cls._envelope.many: ls}
        return cls.do_request("post", path=path, json=json, retry=True)

    @classmethod
    def update(cls, path=None, **kwargs):
        json = {cls._envelope.single: kwargs}
        return cls.do_request("put", path=path, json=json)

    @classmethod
    def list(cls, path=None, **params):
        return cls.do_request("get", path=path, retry=False, **params)
