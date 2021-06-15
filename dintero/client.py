import json

import requests
import time

_dintero_account_id = None
_dintero_api_client_key = None
_dintero_api_client_secret = None
_auth_token = None
_auth_token_expires = 0
_api_url = 'https://api.dintero.com'
_checkout_url = 'https://checkout.dintero.com'
_default_headers = {
    'Dintero-System-Name': 'python-application',
    'Dintero-System-Version': '0.0.0',
    'Dintero-System-Plugin-Name': 'python-sdk',
    'Dintero-System-Plugin-Version': '0.0.0'
}


class AuthError(Exception):
    def __init__(self, message, status_code, headers, body):
        self.message = message
        self.status_code = status_code
        self.headers = headers
        self.body = body

    def __str__(self):
        return self.message + ' ' + str(self.status_code) + ' ' + self.body

class InvalidRequestBody(Exception):
    def __init__(self, message, status_code, headers, body):
        self.message = message
        self.status_code = status_code
        self.headers = headers
        self.body = body

    def __str__(self):
        return self.message + ' ' + str(self.status_code) + ' ' + self.body


class UnexpectedError(Exception):
    pass


def init(account_id, api_key, api_secret, application_name=None, application_version=None):
    global _dintero_account_id
    global _dintero_api_client_key
    global _dintero_api_client_secret
    _dintero_account_id = account_id
    _dintero_api_client_key = api_key
    _dintero_api_client_secret = api_secret

    custom_headers = {}
    if application_name:
        custom_headers['Dintero-System-Name'] = application_name
    if application_version:
        custom_headers['Dintero-System-Version'] = application_version
    _default_headers.update(custom_headers)


def _get_dintero_auth_token():
    global _auth_token
    global _auth_token_expires
    if _auth_token and _auth_token_expires > time.time():
        return _auth_token
    response = requests.post(
        f'{_api_url}/v1/accounts/{_dintero_account_id}/auth/token',
        auth=requests.auth.HTTPBasicAuth(_dintero_api_client_key, _dintero_api_client_secret),
        headers={
            'Content-Type': 'application/json',
        },
        data=json.dumps({
            'grant_type': 'client_credentials',
            'audience': f'https://api.dintero.com/v1/accounts/{_dintero_account_id}'
        })
    )
    _verify_response(response, 200)
    _auth_token = response.json()['token']
    _buffer = 60 * 10
    _auth_token_expires = time.time() + auth_token_response.expires_in - buffer
    return _auth_token


def _get_dintero_auth_header():
    token = _get_dintero_auth_token()
    return f'Bearer {token}'


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

    if response != expected_status_code:
        raise UnexpectedError(
            "Received unexpected server response",
            status_code=response.status_code,
            headers=response.headers,
            body=response.text
        )


def post_session(session):
    # Creates a new payment session

    url = f'{_checkout_url}/v1/sessions'
    if 'profile_id' in session and session['profile_id']:
        # Override and use sessions-profile endpoint
        url = f'{_checkout_url}/v1/sessions-profile'

    response = requests.post(
        url,
        headers=({
            'Authorization': _get_dintero_auth_header(),
            'Content-Type': 'application/json',
            **_default_headers,
        }),
        data=json.dumps(session)
    )
    _verify_response(response, 200)

    return response.json()
