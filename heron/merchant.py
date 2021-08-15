from .base import BaseResource, Envelope


class Merchant(BaseResource):
    _envelope = Envelope("merchant", "merchants")
    _path = "merchants"
    _prefix = "mrc_"

    def __repr__(self):
        return f"<Merchant {self.heron_id}: {self.name}>"

    def __init__(self, **kwargs):
        self.heron_id = kwargs.get("heron_id")
        self.name = kwargs.get("name")
        self.url = kwargs.get("url")
        self.logo_url = kwargs.get("logo_url")
        self.icon_url = kwargs.get("icon_url")

    @classmethod
    def create(cls, *args, **kwargs):
        raise NotImplementedError("cannot create merchant")

    @classmethod
    def create_many(cls, *args, **kwargs):
        raise NotImplementedError("cannot create merchants")

    @classmethod
    def update(cls, *args, **kwargs):
        raise NotImplementedError(
            "cannot update merchant directly, try the Transaction.feedback "
            "endpoint to provide merchant feedback for a merchant match"
        )

    @classmethod
    def list(cls, *args, **kwargs):
        raise NotImplementedError("cannot list merchants, use Merchant.search instead")

    @classmethod
    def search(cls, *, name):
        return super().list(path="merchants/search", name=name)
