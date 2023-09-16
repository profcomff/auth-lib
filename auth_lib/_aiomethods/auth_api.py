from typing import Any
from urllib.parse import urljoin

import aiohttp

from auth_lib.exceptions import AuthFailed, SessionExpired


class AsyncAuthAPILib:
    auth_url: str

    def __init__(self, *, auth_url: str | None = None):
        super().__init__()
        self.auth_url = auth_url

    async def email_login(self, email: str, password: str) -> dict[str, Any]:
        json = {"email": email, "password": password}
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                url=urljoin(self.auth_url, "email/login"), json=json
            )
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
            headers=headers,
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
                url=urljoin(self.auth_url, "logout"), headers=headers
            )

        match response.status:
            case 200:
                return True
            case 401:
                raise AuthFailed(response=await response.json())
            case 403:
                raise SessionExpired(response=await response.json())
