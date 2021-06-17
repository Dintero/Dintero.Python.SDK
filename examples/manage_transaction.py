from dintero import Dintero
import os

account_id = os.environ.get("DINTERO_ACCOUNT_ID")
client_id = os.environ.get("DINTERO_CLIENT_ID")
client_secret = os.environ.get("DINTERO_CLIENT_SECRET")
profile_id = os.environ.get("DINTERO_PROFILE_ID")

dintero = Dintero(account_id, client_id, client_secret)

checkout = dintero.checkout()
transaction_id = os.environ.get("DINTERO_TRANSACTION_ID")
transaction = checkout.capture_transaction(transaction_id)

print(transaction)
