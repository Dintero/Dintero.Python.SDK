from dintero import Dintero
import os

account_id = os.environ.get("DINTERO_ACCOUNT_ID")
client_id = os.environ.get("DINTERO_CLIENT_ID")
client_secret = os.environ.get("DINTERO_CLIENT_SECRET")
profile_id = os.environ.get("DINTERO_PROFILE_ID")

dintero = Dintero(account_id, client_id, client_secret)
checkout = dintero.checkout()
session_info = checkout.create_session(
    {
        "url": {
            "return_url": "https://example.com/accept",
            "callback_url": "https://example.com/callback",
        },
        "order": {
            "amount": 29990,
            "currency": "NOK",
            "merchant_reference": "string",
            "items": [
                {
                    "id": "chair-1",
                    "line_id": "1",
                    "description": "Stablestol",
                    "quantity": 1,
                    "amount": 29990,
                    "vat_amount": 6000,
                    "vat": 25,
                }
            ],
        },
        "profile_id": profile_id,
    }
)

session = checkout.get_session(session_info["id"])

print(session_info)
print(session)
