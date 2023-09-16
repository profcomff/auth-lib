from typing import Any
from urllib.parse import urljoin

import aiohttp


class AsyncUserdataAPILib:
    userdata_url: str

    def __init__(self, *, userdata_url: str | None = None):
        super().__init__()
        self.userdata_url = userdata_url

    async def get_user_data(self, token: str, user_id: int) -> dict[str | Any] | None:
        headers = {"Authorization": token}
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                url=urljoin(self.userdata_url, f"user/{user_id}"), headers=headers
            )
        if response.ok:
            return await response.json()
        return None
