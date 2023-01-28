from typing import Any

import aiohttp

from .exceptions import SessionExpired, AuthFailed, IncorrectData, NotFound


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

    async def check_token(self, token: str) -> dict[str, Any]:
        headers = {"token": token}
        fields = frozenset(["email"])
        async with aiohttp.ClientSession() as session:
            response = await session.post(url=f"{self.url}/me", headers=headers)
        match response.status:
            case 200:
                return await response.json()
            case 400:
                raise IncorrectData(response=await response.json())
            case 404:
                raise NotFound(response=await response.json())
            case 403:
                raise SessionExpired(response=await response.json())

    async def logout(self, token: str) -> bool:
        headers = {"token": token}
        async with aiohttp.ClientSession() as session:
            response = await session.post(url=f"{self.url}/logout", headers=headers)

        match response.status:
            case 200:
                return True
            case 401:
                raise AuthFailed(response=await response.json())
            case 403:
                raise SessionExpired(response=await response.json())
