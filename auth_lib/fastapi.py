from urllib.parse import urljoin

import aiohttp
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security import APIKeyHeader
from fastapi.security.base import SecurityBase
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN


class UnionAuth(SecurityBase):
    model = APIKey.construct(in_=APIKeyIn.header, name="Authorization")
    scheme_name = 'token'
    auth_url = "https://auth.api.test.profcomff.com"

    def __init__(self, auto_error=True) -> None:
        super().__init__()
        self.auto_error = auto_error

    @staticmethod
    def _get_creds(header_value: str):
        if header_value:
            value = header_value.split(maxsplit=2)
        if len(value) == 2:
            return value
        return "token", header_value

    def _except(self):
        if self.auto_error:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
            )
        else:
            return {}

    async def __call__(
            self, request: Request,
            authorization: str = Depends(APIKeyHeader(name="authorization", scheme_name="token"))
    ) -> dict:
        authorization = request.headers.get("authorization")
        if not authorization:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
            )
        scheme, credentials = self._get_creds(authorization)
        if scheme not in ["token"]:
            return self._except()
        async with aiohttp.request(
                'POST',
                urljoin(self.auth_url, '/me'),
                json={"token": credentials}
        ) as r:
            status_code = r.status
            user = await r.json()
        if status_code != 200:
            self._except()
        return user



