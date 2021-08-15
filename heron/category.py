# TODO make as API resource
class Category:
    def __init__(self, **kwargs):
        self.heron_id = kwargs.get("heron_id")
        self.annotator = kwargs.get("annotator")
        self.label = kwargs.get("label")
        self.confidence = kwargs.get("confidence")
