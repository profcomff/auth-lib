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
    allow_none: bool
    scopes: list[str]
    auto_error: bool

    def __init__(
        self,
        auth_url: str,
        auto_error=True,
        allow_none: bool = False,
        scopes: list[str] = [],
    ) -> None:
        super().__init__()
        self.auto_error = auto_error
        self.auth_url = auth_url
        self.allow_none = allow_none
        self.scopes = scopes

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
    ) -> dict[str, str] | None:
        token = request.headers.get("Authorization")
        if not token and self.allow_none:
            return None
        if not token:
            return self._except()
        async with aiohttp.request(
            "GET",
            f"{self.auth_url}/me",
            headers={"Authorization": token},
            params={"info": ["groups", "indirect_groups", "token_scopes", "user_scopes"]},
        ) as r:
            status_code = r.status
            user_session = await r.json()
        if status_code != 200:
            self._except()
        if len(
            set([scope.lower() for scope in self.scopes])
            & set([scope["name"].lower() for scope in user_session["session_scopes"]])
        ) != len(set([scope.lower() for scope in self.scopes])):
            self._except()
        return user_session
