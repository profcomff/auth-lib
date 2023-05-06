from typing import Any
from urllib.parse import urljoin

import aiohttp

from .exceptions import AuthFailed, SessionExpired

# See docs on https://api.test.profcomff.com/?urls.primaryName=auth


class AsyncAuthLib:
    url: str

    def __init__(self, url: str):
        self.url = url

    async def email_login(self, email: str, password: str) -> dict[str, Any]:
        json = {"email": email, "password": password}
        async with aiohttp.ClientSession() as session:
            response = await session.post(url=f"{self.url}/email/login", json=json)
        match response.status:
            case 200:
                return await response.json()
            case 401:
                raise AuthFailed(response=await response.json())

    async def check_token(
        self, token: str
    ) -> dict[str, int | list[dict[str, str | int]]] | None:
        headers = {"Authorization": token}
        async with aiohttp.request(
            "GET",
            urljoin(self.url, "me"),
            headers={"Authorization": token},
            params={
                "info": [
                    "groups",
                    "indirect_groups",
                    "session_scopes",
                    "user_scopes",
                ]
            },
        ) as r:
            status_code = r.status
            user_session = await r.json()
        if status_code == 200:
            return user_session
        return None

    async def logout(self, token: str) -> bool:
        headers = {"Authorization": token}
        async with aiohttp.ClientSession() as session:
            response = await session.post(url=f"{self.url}/logout", headers=headers)

        match response.status:
            case 200:
                return True
            case 401:
                raise AuthFailed(response=await response.json())
            case 403:
                raise SessionExpired(response=await response.json())
