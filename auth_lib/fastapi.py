from urllib.parse import urljoin

import aiohttp
from fastapi.exceptions import HTTPException
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN


class UnionAuth(SecurityBase):
    model = APIKey.construct(in_=APIKeyIn.header, name="Authorization")
    scheme_name = "token"
    auth_url: str

    def __init__(self, auth_url: str, auto_error=True) -> None:
        super().__init__()
        self.auto_error = auto_error
        self.auth_url = auth_url

    def _except(self):
        if self.auto_error:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
            )
        else:
            return {}

    async def __call__(
        self,
        request: Request,
    ) -> dict[str, str]:
        token = request.headers.get("Authorization")
        if not token:
            return self._except()
        async with aiohttp.request(
            "POST",
            urljoin(self.auth_url, "/me"),
            headers={"token": token},
        ) as r:
            status_code = r.status
            user = await r.json()
        if status_code != 200:
            self._except()
        return user
