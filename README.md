# Dintero Python SDK

![Build Status](https://github.com/dintero/Dintero.Python.SDK/actions/workflows/ci.yml/badge.svg)

With the Dintero Python SDK you can easily interact with the Dintero API to create and manage payments through the
Checkout API, and in the future also use the many other APIs we've got.

## Installation

Install from pip by using:

```
pip install --upgrade dintero
```

### Requirements

* Python 3.6+

## Using the SDK

Create an account through https://onboarding.dintero.com.

Get client credentials from the Dintero Backoffice, see [guide](https://docs.dintero.com/docs/checkout/checkout-client).

Create a payment profile by going to [Dintero Backoffice](https://backoffice.dintero.com) --> Settings --> Payment
Profiles

Use your newly created credentials to create a session:

```python
from dintero import Dintero

account_id = 'T12345678'
client_id = '72e023b1-aeda-498e-b141-4669528c44b9'
client_secret = '125f9f0a-e240-4bfd-be57-0086343bf0e4'

profile_id = 'T12345678.46dP6T4F1mUXYPeYKYc5Gj'

dintero = Dintero(
    account_id,
    client_id,
    client_secret)
checkout = dintero.checkout()
session_info = checkout.create_session({
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

print(session_info)
```
