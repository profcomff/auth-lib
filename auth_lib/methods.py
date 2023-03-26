from typing import Any

import requests

from .exceptions import AuthFailed, IncorrectData, NotFound, SessionExpired

# See docs on https://api.test.profcomff.com/?urls.primaryName=auth


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
        headers = {"Authorization": token}
        response = requests.get(
            url=f"{self.url}/me",
            headers=headers,
            params={
                "info": ["groups", "indirect_groups", "session_scopes", "user_scopes"]
            },
        )
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
        headers = {"Authorization": token}
        response = requests.post(url=f"{self.url}/logout", headers=headers)

        match response.status_code:
            case 200:
                return True
            case 401:
                raise AuthFailed(response=response.json()["body"])
            case 403:
                raise SessionExpired(response=response.json()["body"])
