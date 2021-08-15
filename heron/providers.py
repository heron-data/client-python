from .utils import to_dollars, to_iso_format


def from_plaid(t):
    # https://plaid.com/docs/api/products/#transactionsget
    date_or_timestamp = {}
    if timestamp := t.get("datetime"):
        date_or_timestamp = {
            "timestamp": timestamp,
        }
    elif date := t.get("date"):
        date_or_timestamp = {
            "date": date,
        }

    return {
        "account_id": t["account_id"],
        "amount": -t["amount"],
        "categories_default": t["category"],
        "currency": t["iso_currency_code"],
        "description": t["name"],
        "reference_id": t["transaction_id"],
        "transaction_code": t["payment_channel"],
        **date_or_timestamp,
    }


def from_yodlee(t):
    # https://developer.yodlee.com/api-reference#operation/getTransactions
    return {
        "account_id": t["accountId"],
        "amount": to_dollars(t["amount"]["amount"]),
        "date": t["date"],
        "categories_default": t["category"],
        "currency": t["amount"]["currency"],
        "description": t["description"]["original"],
        "reference_id": str(t["id"]),
        "transaction_code": t["type"],
    }


def from_finicity(t):
    # https://api-reference.finicity.com/#/rest/models/structures/transaction
    return {
        "account_id": t["accountId"],
        "amount": t["amount"],
        "categories_default": t["categorization"]["category"],
        "timestamp": to_iso_format(t["postedDate"]),
        "description": t["description"],
        "reference_id": str(t["id"]),
        "transaction_code": t["type"],
    }


def from_truelayer(t):
    # https://docs.truelayer.com/#retrieve-account-transactions
    return {
        "account_id": t["account_id"],
        "amount": t["amount"],
        "categories_default": t["transaction_classification"],
        "currency": t["currency"],
        "description": t["description"],
        "reference_id": str(t["transaction_id"]),
        "timestamp": t["timestamp"],
        "transaction_code": t["transaction_category"],
    }


PROVIDER_HANDLER = {
    "finicity": from_finicity,
    "plaid": from_plaid,
    "truelayer": from_truelayer,
    "yodlee": from_yodlee,
}
