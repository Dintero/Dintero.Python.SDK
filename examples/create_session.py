from dintero import Dintero
import os

account_id = os.environ.get('DINTERO_ACCOUNT_ID')
client_id = os.environ.get("DINTERO_CLIENT_ID")
client_secret = os.environ.get("DINTERO_CLIENT_SECRET")
profile_id = os.environ.get("DINTERO_PROFILE_ID")

api_url = 'https://api.dintero.com'
if "DINTERO_API_URL" in os.environ:
    api_url = os.environ.get('DINTERO_API_URL')

checkout_url = 'https://checkout.dintero.com'
if "DINTERO_CHECKOUT_URL" in os.environ:
    checkout_url = os.environ.get('DINTERO_CHECKOUT_URL')

dintero = Dintero(
    account_id,
    client_id,
    client_secret,
    api_url=api_url,
    checkout_url=checkout_url)
checkout = dintero.checkout()
session_info = checkout.post_session({
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

session = checkout.get_session(session_info['id'])

print(session)
