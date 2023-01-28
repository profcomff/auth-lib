from typing import Any

import requests

from .exceptions import SessionExpired, AuthFailed, IncorrectData, NotFound


# See docs on https://auth.api.test.profcomff.com/docs


class AuthLib:
    url: str

    def __init__(self, url: str):
        self.url = url

    def email_login(self, email: str, password: str) -> dict[str, Any]:
        json = {"email": email, "password": password}
        response = requests.post(url=f"{self.url}/email/login", json=json)
        match response.status_code:
            case 200:
                return response.json()
            case 401:
                raise AuthFailed(response=response.json()["body"])

    def check_token(self, token: str) -> dict[str, Any]:
        headers = {"token": token}
        fields = frozenset(["email"])
        response = requests.post(url=f"{self.url}/me", headers=headers)
        match response.status_code:
            case 200:
                return response.json()
            case 400:
                raise IncorrectData(response=response.json()["body"])
            case 404:
                raise NotFound(response=response.json()["body"])
            case 403:
                raise SessionExpired(response=response.json()["body"])

    def logout(self, token: str) -> bool:
        headers = {"token": token}
        response = requests.post(url=f"{self.url}/logout", headers=headers)

        match response.status_code:
            case 200:
                return True
            case 401:
                raise AuthFailed(response=response.json()["body"])
            case 403:
                raise SessionExpired(response=response.json()["body"])
