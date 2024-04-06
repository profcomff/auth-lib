from typing import Any
from urllib.parse import urljoin

import requests

from .exceptions import AuthFailed, SessionExpired

# See docs on https://api.test.profcomff.com/?urls.primaryName=auth


class AuthLib:
    auth_url: str
    userdata_url: str

    def __init__(self, *, auth_url: str | None = None, userdata_url: str | None = None):
        self.auth_url = auth_url
        self.userdata_url = userdata_url

    def email_login(self, email: str, password: str) -> dict[str, Any]:
        json = {"email": email, "password": password}
        response = requests.post(url=urljoin(self.auth_url, "email/login"), json=json)
        match response.status_code:
            case 200:
                return response.json()
            case 401:
                raise AuthFailed(response=response.json()["body"])

    def check_token(self, token: str) -> dict[str, Any] | None:
        headers = {"Authorization": token}
        response = requests.get(
            url=urljoin(self.auth_url, "me"),
            headers=headers,
            params={
                "info": [
                    "indirect_groups",
                    "session_scopes",
                ]
            },
        )
        if response.ok:
            return response.json()
        return None

    def logout(self, token: str) -> bool:
        headers = {"Authorization": token}
        response = requests.post(url=urljoin(self.auth_url, "logout"), headers=headers)
        match response.status_code:
            case 200:
                return True
            case 401:
                raise AuthFailed(response=response.json()["body"])
            case 403:
                raise SessionExpired(response=response.json()["body"])

    def get_user_data(self, token: str, user_id: int) -> dict[str | Any] | None:
        headers = {"Authorization": token}
        response = requests.get(
            url=urljoin(self.userdata_url, f"user/{user_id}"), headers=headers
        )
        if response.ok:
            return response.json()
        return None
