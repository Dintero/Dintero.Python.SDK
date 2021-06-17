import json

import requests
import time

from dintero.error import InvalidRequestBody, AuthError, UnexpectedError

_default_headers = {
    'Dintero-System-Name': 'python-application',
    'Dintero-System-Version': '0.0.0',
    'Dintero-System-Plugin-Name': 'python-sdk',
    'Dintero-System-Plugin-Version': '0.0.0'
}


class Checkout:
    def __init__(self,
                 api_url,
                 checkout_url,
                 account_id,
                 client_id,
                 client_secret,
                 application_name,
                 application_version):
        self.api_url = api_url
        self.checkout_url = checkout_url
        self.account_id = account_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_token_expires = 0
        self.auth_token = None
        custom_headers = {
            'Dintero-System-Name': application_name,
            'Dintero-System-Version': application_version
        }
        _default_headers.update(custom_headers)

    def get_dintero_auth_token(self):
        if self.auth_token and self.auth_token_expires > time.time():
            return self.auth_token

        url = f'{self.api_url}/v1/accounts/{self.account_id}/auth/token'
        payload = {
            'grant_type': 'client_credentials',
            'audience': f'{self.api_url}/v1/accounts/{self.account_id}'
        }
        response = requests.post(
            url,
            auth=requests.auth.HTTPBasicAuth(self.client_id, self.client_secret),
            headers={
                'Content-Type': 'application/json',
            },
            data=json.dumps(payload)
        )
        _verify_response(response, 200)
        auth_token_response = response.json()
        self.auth_token = auth_token_response['access_token']
        _buffer = 60 * 10
        self.auth_token_expires = time.time() + auth_token_response['expires_in'] - _buffer
        return self.auth_token

    def _get_dintero_auth_header(self):
        token = self.get_dintero_auth_token()
        return f'Bearer {token}'

    def post_session(self, session):
        # Creates a new payment session

        url = f'{self.checkout_url}/v1/sessions'
        if 'profile_id' in session and session['profile_id']:
            # Override and use sessions-profile endpoint
            url = f'{self.checkout_url}/v1/sessions-profile'

        response = requests.post(
            url,
            headers=({
                'Authorization': self._get_dintero_auth_header(),
                'Content-Type': 'application/json',
                **_default_headers,
            }),
            data=json.dumps(session)
        )
        _verify_response(response, 200)
        return response.json()

    def get_session(self, session_id: str):
        url = f'{self.checkout_url}/v1/sessions/{session_id}'
        response = requests.get(
            url,
            headers=({
                'Authorization': self._get_dintero_auth_header(),
                'Content-Type': 'application/json',
                **_default_headers,
            })
        )
        _verify_response(response, 200)
        return response.json()


def _verify_response(response, expected_status_code):
    if response.status_code == 400:
        raise InvalidRequestBody(
            "Body is malformed",
            status_code=response.status_code,
            headers=response.headers,
            body=response.text
        )

    if response.status_code in [401, 403]:
        raise AuthError(
            "Auth failed",
            status_code=response.status_code,
            headers=response.headers,
            body=response.text
        )

    if response.status_code != expected_status_code:
        raise UnexpectedError(
            "Received unexpected server response",
            status_code=response.status_code,
            headers=response.headers,
            body=response.text
        )
