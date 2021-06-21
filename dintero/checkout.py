import json
from typing import List, Union
import requests
import time

from dintero.error import InvalidRequestBody, AuthError, UnexpectedError
from dintero.types import Item
from dintero.validator import validate_session

_default_headers = {
    "Dintero-System-Name": "python-application",
    "Dintero-System-Version": "0.0.0",
    "Dintero-System-Plugin-Name": "python-sdk",
    "Dintero-System-Plugin-Version": "0.0.0",
}


class Checkout:
    """
    Dintero Checkout client

    Contains methods to interact with the Dintero Checkout API
    """

    def __init__(
        self,
        api_url,
        checkout_url,
        account_id,
        client_id,
        client_secret,
        application_name,
        application_version,
    ):
        self.api_url = api_url
        self.checkout_url = checkout_url
        self.account_id = account_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_token_expires = 0
        self.auth_token = None
        custom_headers = {
            "Dintero-System-Name": application_name,
            "Dintero-System-Version": application_version,
        }
        _default_headers.update(custom_headers)

    def create_session(self, session):
        """
        Create a session

        Create a corresponding Checkout Session for an order from your system

        A session can have multiple payment types.

        If the session contains a profile_id, the configuration from
        the profile_id will be used.

        :param session: The payload of the session to create
        :return: The id of the session and an URL to redirect to
        """
        validate_session(session)
        url = f"{self.checkout_url}/v1/sessions"
        if "profile_id" in session and session["profile_id"]:
            # Override and use sessions-profile endpoint
            url = f"{self.checkout_url}/v1/sessions-profile"

        response = requests.post(
            url,
            headers=(
                {
                    "Authorization": self._get_dintero_auth_header(),
                    "Content-Type": "application/json",
                    **_default_headers,
                }
            ),
            data=json.dumps(session),
        )
        _verify_response(response, 200)
        return response.json()

    def get_session(self, session_id: str):
        url = f"{self.checkout_url}/v1/sessions/{session_id}"
        response = requests.get(
            url,
            headers=(
                {
                    "Authorization": self._get_dintero_auth_header(),
                    "Content-Type": "application/json",
                    **_default_headers,
                }
            ),
        )
        _verify_response(response, 200)
        return response.json()

    def get_transaction(self, transaction_id: str):
        """
        Get a transaction by its transaction_id

        When a session is paid, it will contain a transaction_id.
        A session can only have one transaction.

        The transaction_id will also be sent in the return_url and
        callback_url.

        :param transaction_id: The ID of the transaction
        :return: The transaction
        """
        url = f"{self.checkout_url}/v1/transactions/{transaction_id}"
        response = requests.get(
            url,
            headers=(
                {
                    "Authorization": self._get_dintero_auth_header(),
                    "Content-Type": "application/json",
                    **_default_headers,
                }
            ),
        )
        _verify_response(response, 200)
        return response.json()

    def void_transaction(self, transaction_id: str):
        """Voiding transactions

        At any moment before capture of a transaction,
        it is possible to cancel an authorization.
        This operation is called voiding.

        Void on part capture

        Calling void after a part capture will cancel the difference between
        the captured and authorized amount.

        Void on part capture is only supported on payex.creditcard
        transactions

        :param transaction_id: ID of the transaction to void
        :return: The updated transaction
        """
        url = f"{self.checkout_url}/v1/transactions/{transaction_id}/void"
        response = requests.post(
            url,
            headers=(
                {
                    "Authorization": self._get_dintero_auth_header(),
                    "Content-Type": "application/json",
                    **_default_headers,
                }
            ),
        )
        _verify_response(response, 200)
        return response.json()

    def capture_transaction(
        self,
        transaction_id: str,
        amount: int,
        items: List[Item],
        capture_reference: Union[str, None] = None,
    ):
        """
        Captures a transaction that is either authorized or partially captured

        :param transaction_id: The ID of the transaction
        :param amount: The amount to capture, up to the full
        amount of the transaction
        :param items: The items to capture, must correspond with the
        items of the session
        :param capture_reference: Optional unique reference to
        the capture event
        :return: The updated transaction
        """
        url = f"{self.checkout_url}/v1/transactions/{transaction_id}/capture"

        payload = {
            "amount": amount,
            "items": items,
        }
        if capture_reference is not None:
            payload["capture_reference"] = capture_reference
        response = requests.post(
            url,
            headers=(
                {
                    "Authorization": self._get_dintero_auth_header(),
                    "Content-Type": "application/json",
                    **_default_headers,
                }
            ),
            data=json.dumps(payload),
        )
        _verify_response(response, 200)
        return response.json()

    def refund_transaction(
        self,
        transaction_id: str,
        amount: int,
        items: List[Item],
        refund_reference: Union[str, None] = None,
        reason: Union[str, None] = None,
    ):
        """
        Once a transaction has been successfully captured, a refund operation
        is available. Like other operations, refund can be partial or total

        :param transaction_id: The ID of the transaction
        :param amount: The amount to refund, up to the captured amount
        :param items: The items to refund, must correspond with the items
        of the session
        :param refund_reference: Optional unique reference to the refund event
        :param reason: Optional free text field to describe the refund reason
        :return: The updated transaction
        """
        url = f"{self.checkout_url}/v1/transactions/{transaction_id}/refund"

        payload = {
            "amount": amount,
            "items": items,
        }
        if refund_reference is not None:
            payload["refund_reference"] = refund_reference
        if reason is not None:
            payload["reason"] = reason
        response = requests.post(
            url,
            headers=(
                {
                    "Authorization": self._get_dintero_auth_header(),
                    "Content-Type": "application/json",
                    **_default_headers,
                }
            ),
            data=json.dumps(payload),
        )
        _verify_response(response, 200)
        return response.json()

    def _get_dintero_auth_token(self):
        if self.auth_token and self.auth_token_expires > time.time():
            return self.auth_token

        url = f"{self.api_url}/v1/accounts/{self.account_id}/auth/token"
        payload = {
            "grant_type": "client_credentials",
            "audience": f"{self.api_url}/v1/accounts/{self.account_id}",
        }
        response = requests.post(
            url,
            auth=requests.auth.HTTPBasicAuth(
                self.client_id, self.client_secret
            ),
            headers={
                "Content-Type": "application/json",
            },
            data=json.dumps(payload),
        )
        _verify_response(response, 200)
        auth_token_response = response.json()
        self.auth_token = auth_token_response["access_token"]
        _buffer = 60 * 10
        self.auth_token_expires = (
            time.time() + auth_token_response["expires_in"] - _buffer
        )
        return self.auth_token

    def _get_dintero_auth_header(self):
        token = self._get_dintero_auth_token()
        return f"Bearer {token}"


def _verify_response(response, expected_status_code):
    if response.status_code == 400:
        raise InvalidRequestBody(
            "Body is malformed",
            status_code=response.status_code,
            headers=response.headers,
            body=response.text,
        )

    if response.status_code in [401, 403]:
        raise AuthError(
            "Auth failed",
            status_code=response.status_code,
            headers=response.headers,
            body=response.text,
        )

    if response.status_code != expected_status_code:
        raise UnexpectedError(
            "Received unexpected server response",
            status_code=response.status_code,
            headers=response.headers,
            body=response.text,
        )
