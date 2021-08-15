import os

import heron

heron.basic_auth_username = os.getenv("HERON_USERNAME")
heron.basic_auth_password = os.getenv("HERON_PASSWORD")
heron.provider = "plaid"

end_user = heron.EndUser.create(
    name="Spotify UK",
    end_user_id="my-internal-system-uuid",
)

transaction = heron.Transaction.create(
    amount=11.11,
    description="Spotify UK",
    end_user=end_user,
)

transactions = heron.Transaction.create_many(
    transactions=[
        {
            "amount": 11.11,
            "description": "Stripe payment to XYZ",
        }
    ],
    end_user=end_user,
)

end_user.update(status="ready")

transactions = heron.Transaction.list(end_user_id=end_user.end_user_id, limit=100)

categories = heron.Category.list()
merchants = heron.Merchant.search(name="Netflix")

transactions = heron.Transaction.feedback(
    transaction=transaction,
    category=categories[0],
    merchant=merchants[0],
)
