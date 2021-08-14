# TODO make API resource
class Merchant:
    def __init__(self, **kwargs):
        self.heron_id = kwargs.get("heron_id")
        self.name = kwargs.get("name")
        self.url = kwargs.get("url")
        self.logo_url = kwargs.get("logo_url")
        self.icon_url = kwargs.get("icon_url")
