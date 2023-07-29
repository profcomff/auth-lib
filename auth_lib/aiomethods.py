from typing import Any
from urllib.parse import urljoin

import aiohttp

from .exceptions import AuthFailed, IncorrectData, NotFound, SessionExpired

# See docs on https://api.test.profcomff.com/?urls.primaryName=auth


class AsyncAuthLib:
    auth_url: str
    user_data_url: str

    def __init__(self, url: str):
        self.auth_url = url

    async def email_login(self, email: str, password: str) -> dict[str, Any]:
        json = {"email": email, "password": password}
        async with aiohttp.ClientSession() as session:
            response = await session.post(url=f"{self.auth_url}/email/login", json=json)
        match response.status:
            case 200:
                return await response.json()
            case 401:
                raise AuthFailed(response=await response.json())

    async def check_token(self, token: str) -> dict[str, Any] | None:
        headers = {"Authorization": token}
        async with aiohttp.request(
            "GET",
            urljoin(self.auth_url, "me"),
            headers={"Authorization": token},
            params={
                "info": [
                    "indirect_groups",
                    "session_scopes",
                ]
            },
        ) as r:
            user_session = await r.json()
        if r.ok:
            return user_session
        return None

    async def logout(self, token: str) -> bool:
        headers = {"Authorization": token}
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                url=f"{self.auth_url}/logout", headers=headers
            )

        match response.status:
            case 200:
                return True
            case 401:
                raise AuthFailed(response=await response.json())
            case 403:
                raise SessionExpired(response=await response.json())

    async def get_user_data(self, token: str) -> dict[str | Any] | None:
        headers = {"Authorization": token}
        user_get = await self.check_token(token)
        user_id = user_get["id"]
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                url=f"{self.user_data_url}/user/{user_id}", headers=headers
            )
        match response.status:
            case 200:
                return await response.json()
            case 403:
                raise SessionExpired(response=response.json()["body"])
            case 404:
                raise NotFound(response=response.json()["body"])
            case 422:
                raise IncorrectData(response=response.json()["body"])
        return None
