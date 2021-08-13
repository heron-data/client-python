from datetime import datetime

from .base import BaseResource, Envelope


class Transaction(BaseResource):
    _envelope = Envelope("transaction", "transactions")
    _path = "transactions"

    def __init__(self, **data):
        from .category import Category
        from .merchant import Merchant

        self.heron_id = data.get("heron_id")
        self.amount = data.get("amount")
        self.timestamp = (
            datetime.fromisoformat(t) if (t := data.get("timestamp")) else None
        )
        self.description = data.get("description")
        self.description_clean = data.get("description_clean")
        self.counterparty = data.get("description_clean")
        self.categories = [Category(**c) for c in data.get("categories", [])]
        self.merchant = Merchant(**m) if (m := data.get("merchant")) else None
        self.payment_processor = (
            Merchant(**p) if (p := data.get("payment_processor")) else None
        )

    @classmethod
    def create(cls, end_user_id=None, name=None):
        raise NotImplementedError("use Transaction.create_many")

    @classmethod
    def create_many(cls, transactions):
        if not isinstance(transactions, list):
            raise ValueError("create_many needs a list")
        if not transactions:
            raise ValueError("no transactions to create")
        if not all(isinstance(t, dict) for t in transactions):
            raise ValueError("transactions must be a list of dicts")
        if not all("description" in t and "amount" in t for t in transactions):
            raise ValueError("'description' and 'amount' are required")

        return super().create_many(transactions)

    @classmethod
    def update(cls, end_user_id=None, name=None, status="new"):
        return super().update(end_user_id=end_user_id, name=name, status=status)

    @classmethod
    def list(cls, page=None, limit=None):
        return super().list(page=page, limit=limit)
