from dintero import client
import os

account_id = os.environ.get('DINTERO_ACCOUNT_ID')
client_id = os.environ.get("DINTERO_CLIENT_ID")
client_secret = os.environ.get("DINTERO_CLIENT_SECRET")
profile_id = os.environ.get("DINTERO_PROFILE_ID")

if "DINTERO_API_URL" in os.environ:
    client._api_url = os.environ.get('DINTERO_API_URL')

if "DINTERO_CHECKOUT_URL" in os.environ:
    client._checkout_url = os.environ.get('DINTERO_CHECKOUT_URL')

client.init(account_id, client_id, client_secret, 'example', '1.0.0')
session = client.post_session({
    "url": {
        "return_url": "https://example.com/accept",
        "callback_url": "https://example.com/callback"
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
                "vat": 25
            }
        ]
    },
    "profile_id": profile_id
})

print(session)
