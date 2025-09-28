"""Script to connect to Auth0 and retrieve an access token."""

import base64
import hashlib
import os
import secrets

import requests
from dotenv import load_dotenv

load_dotenv()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")


def generate_pkce_verifier():
    """Generate a PKCE code verifier."""

    verifier = secrets.token_urlsafe(64)
    return verifier


def generate_pkce_challenge(verifier):
    """Generate a PKCE code challenge from the verifier."""

    sha256 = hashlib.sha256(verifier.encode("utf-8")).digest()
    challenge = base64.urlsafe_b64encode(sha256).rstrip(b"=").decode("utf-8")
    return challenge


def get_authorization_code(pkce_challenge, state="some_random_state"):
    """Get an authorization code from Auth0 using PKCE."""
    base_url = f"https://{AUTH0_DOMAIN}/authorize"
    request_params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "state": "some_random_state",
        "redirect_uri": "https://example-app.com/redirect",
        "code_challenge": pkce_challenge,
        "code_challenge_method": "S256",
    }
    response = requests.Request("GET", base_url, params=request_params).prepare()
    print(f"Go to the following URL to authorize:\n{response.url}")
    authorization_code = input("Enter the authorization code: ")
    return authorization_code


if __name__ == "__main__":
    pkce_verifier = generate_pkce_verifier()
    pkce_challenge = generate_pkce_challenge(pkce_verifier)

    print(f"PKCE Verifier: {pkce_verifier}")
    print(f"PKCE Challenge: {pkce_challenge}")

    state = secrets.token_urlsafe(16)
    print(f"State: {state}")
    authorization_code = get_authorization_code(pkce_challenge, state)
    print(f"Authorization Code: {authorization_code}")

    # token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    # headers = {"Content-Type": "application/json"}
    # data = {
    #     "grant_type": "client_credentials",
    #     "client_id": AUTH0_CLIENT_ID,
    #     "client_secret": AUTH0_CLIENT_SECRET,
    #     "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
    # }

    # response = requests.post(token_url, json=data, headers=headers)
    # response.raise_for_status()

    # access_token = response.json().get("access_token")
    # print(f"Access Token: {access_token}")
