from .base import BaseResource, Envelope


class Category(BaseResource):
    _envelope = Envelope("category", "categories")
    _path = "categories"
    _prefix = "ctg_"

    def __repr__(self):
        return f"<Category {self.heron_id}: {self.label}>"

    def __init__(self, **kwargs):
        self.heron_id = kwargs.get("heron_id")
        self.annotator = kwargs.get("annotator")
        self.label = kwargs.get("label")
        self.confidence = kwargs.get("confidence")
        self.model_version = kwargs.get("model_version")

    @classmethod
    def create(cls, *args, **kwargs):
        raise NotImplementedError("categories are created during onboarding")

    @classmethod
    def create_many(cls, *args, **kwargs):
        raise NotImplementedError("categories are created during onboarding")

    @classmethod
    def update(cls, *args, **kwargs):
        raise NotImplementedError("please contact us to update your categories")

    @classmethod
    def list(cls):
        return super().list()
