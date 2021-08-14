import heron

heron.basic_auth_username = "user"
heron.basic_auth_password = "pw"
heron.data_source = "plaid"

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

transactions = heron.Transaction.feedback(
    transaction=transaction,
    category="Expenses",
    merchant="Netflix",
)
