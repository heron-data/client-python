import warnings

from .base import BaseResource, Envelope
from .category import Category
from .merchant import Merchant
from .providers import PROVIDER_HANDLER


class Transaction(BaseResource):
    _envelope = Envelope("transaction", "transactions")
    _path = "transactions"
    _prefix = "txn_"

    def __repr__(self):
        return f"<Transaction {self.heron_id}: {self.description}>"

    def __init__(self, **data):
        self.heron_id = data.get("heron_id")
        self.account_id = data.get("account_id")
        self.end_user_id = data.get("end_user_id")
        self.reference_id = data.get("reference_id")

        self.amount = data.get("amount")
        self.currency = data.get("currency")
        self.timestamp = data.get("timestamp")

        self.description = data.get("description")
        self.description_clean = data.get("description_clean")
        self.counterparty = data.get("description_clean")

        self.categories = [Category(**c) for c in data.get("categories", [])]

        self.merchant = Merchant(**m) if (m := data.get("merchant")) else None
        self.payment_processor = (
            Merchant(**p) if (p := data.get("payment_processor")) else None
        )

        self.mcc_code = data.get("mcc_code")
        self.mcc = data.get("mcc_code")
        self.transaction_code = data.get("transaction_code")

        self.has_matching_transaction = data.get("has_matching_transaction")
        self.is_potential_duplicate = data.get("is_potential_duplicate")
        self.is_recurring = data.get("is_recurring")

    @staticmethod
    def _parse_transactions(transactions):
        from heron import provider

        if not provider:
            return transactions

        provider_slug = provider.lower().replace(" ", "-")
        try:
            parse_function = PROVIDER_HANDLER[provider_slug]
        except KeyError as e:
            warnings.warn(
                f"provider '{e}' not supported, will not apply format conversion",
                UserWarning,
            )
            return transactions

        return [parse_function(t) for t in transactions]

    @classmethod
    def create(cls, end_user=None, **data):
        return cls.create_many([data], end_user=end_user)[0]

    @classmethod
    def create_many(cls, transactions, end_user=None):
        from .end_user import EndUser

        if not isinstance(transactions, list):
            raise ValueError("create_many needs a list")
        if not transactions:
            raise ValueError("no transactions to create")
        if not all(isinstance(t, dict) for t in transactions):
            raise ValueError("transactions must be a list of dicts")

        transactions = cls._parse_transactions(transactions)
        if end_user:
            if isinstance(end_user, EndUser) and not end_user.end_user_id:
                raise ValueError("end_user object must have an end_user_id")

            if isinstance(end_user, EndUser):
                end_user_id = end_user.end_user_id
            elif isinstance(end_user, str):
                end_user_id = end_user
            else:
                raise ValueError("end_user must be a valid end_user_id or object")

            transactions = [
                {
                    **t,
                    **{"end_user_id": end_user_id},
                }
                for t in transactions
            ]
        if not all("description" in t and "amount" in t for t in transactions):
            raise ValueError("'description' and 'amount' are required")

        return super().create_many(transactions)

    @classmethod
    def feedback(cls, *, transaction, merchant=None, category=None):
        if isinstance(transaction, Transaction):
            transaction = transaction.heron_id
        if not isinstance(transaction, str):
            raise ValueError("transaction must be a string or Transaction object")
        if not transaction.startswith(cls._prefix):
            raise ValueError(f"invalid heron_id, must start with '{cls._prefix}'")

        if not merchant and not category:
            raise ValueError("either merchant or category required for feedback")

        kwargs = {}
        if merchant is not None:
            if isinstance(merchant, Merchant) and merchant.heron_id:
                merchant = {"heron_id": merchant.heron_id}
            elif isinstance(merchant, str) and merchant.startswith("mrc_"):
                merchant = {"heron_id": merchant}
            elif isinstance(merchant, str):
                merchant = {"name": merchant}
            else:
                raise ValueError("merchant must be a valid string or object")
            kwargs.update({"merchant": merchant})

        if category is not None:
            if isinstance(category, Category) and category.heron_id:
                category = {"heron_id": category.heron_id}
            elif isinstance(category, str) and category.startswith("ctg_"):
                category = {"heron_id": category}
            elif isinstance(category, str):
                category = {"label": category}
            else:
                raise ValueError("category must be a valid string or object")
            kwargs.update({"category": category})

        super().update(path=f"transactions/{transaction}/feedback", **kwargs)
