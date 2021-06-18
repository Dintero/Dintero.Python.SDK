from dintero.checkout import Checkout


class Dintero:
    def __init__(
        self,
        account_id,
        client_id,
        client_secret,
        application_name="python-application",
        application_version="0.0.0",
        api_url="https://api.dintero.com",
        checkout_url="https://checkout.dintero.com",
    ):
        self.api_url = api_url
        self.checkout_url = checkout_url
        self.account_id = account_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.checkout_client = None
        self.application_name = application_name
        self.application_version = application_version

    def checkout(self):
        if self.checkout_client is None:
            self.checkout_client = Checkout(
                self.api_url,
                self.checkout_url,
                self.account_id,
                self.client_id,
                self.client_secret,
                self.application_name,
                self.application_version,
            )
        return self.checkout_client
