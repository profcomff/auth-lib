from typing import Any
from warnings import warn

from fastapi.exceptions import HTTPException
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase
from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN

from auth_lib.aiomethods import AsyncAuthLib


class UnionAuthSettings(BaseSettings):
    AUTH_URL: str = "https://api.test.profcomff.com/auth/"
    AUTH_AUTO_ERROR: bool = True
    AUTH_ALLOW_NONE: bool = False
    model_config = ConfigDict(case_sensitive=True, env_file=".env", extra="ignore")


class UnionAuth(SecurityBase):
    model = APIKey.construct(in_=APIKeyIn.header, name="Authorization")
    scheme_name = "token"
    settings = UnionAuthSettings()

    def __init__(
        self,
        scopes: list[str] = [],
        auto_error: bool | None = None,
        allow_none: bool | None = None,
        auth_url=None,  # Для обратной совместимости
    ) -> None:
        if auth_url is not None:
            warn(
                "auth_url in args deprecated, use AUTH_URL env instead",
                DeprecationWarning,
            )
        super().__init__()
        self.auth_url = auth_url or self.settings.AUTH_URL
        if not self.auth_url.endswith("/"):
            self.auth_url = self.auth_url + "/"
        self.auto_error = (
            auto_error if auto_error is not None else self.settings.AUTH_AUTO_ERROR
        )
        self.allow_none = (
            allow_none if allow_none is not None else self.settings.AUTH_ALLOW_NONE
        )
        self.scopes = scopes

    def _except(self):
        if self.auto_error:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
            )
        else:
            return None

    async def _get_session(self, token: str | None) -> dict[str, Any] | None:
        if not token and self.allow_none:
            return None
        if not token:
            return self._except()
        return await AsyncAuthLib(url=self.auth_url).check_token(token)

    async def __call__(
        self,
        request: Request,
    ) -> dict[str, Any] | None:
        token = request.headers.get("Authorization")
        user_session = await self._get_session(token)
        if user_session is None:
            return self._except()
        session_scopes = set(
            [scope["name"].lower() for scope in user_session["session_scopes"]]
        )
        required_scopes = set([scope.lower() for scope in self.scopes])
        if required_scopes - session_scopes:
            self._except()
        return user_session
