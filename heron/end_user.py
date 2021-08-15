from .base import BaseResource, Envelope


class EndUser(BaseResource):
    _envelope = Envelope("end_user", "end_users")
    _path = "end_users"

    def __init__(self, **data):
        self.heron_id = data.get("heron_id")
        self.name = data.get("name")
        self.end_user_id = data.get("end_user_id")
        self.reference_id = data.get("end_user_id")
        self.status = data.get("status")

    @classmethod
    def create(cls, end_user_id=None, name=None):
        if not end_user_id:
            raise ValueError("end_user_id must not be None")
        return super().create(end_user_id=end_user_id, name=name, status="new")

    @classmethod
    def create_many(cls, ls):
        raise NotImplementedError("use EndUser.create")

    @classmethod
    def update(cls, end_user_id=None, name=None, status="new"):
        return super().update(end_user_id=end_user_id, name=name, status=status)

    @classmethod
    def list(cls, page=None, limit=None):
        return super().list(page=page, limit=limit)
