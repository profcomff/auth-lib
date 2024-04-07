from typing import Any
from warnings import warn

from fastapi.exceptions import HTTPException
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase
from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from auth_lib.aiomethods import AsyncAuthLib


class UnionAuthSettings(BaseSettings):
    AUTH_URL: str = "https://api.test.profcomff.com/auth/"
    USERDATA_URL: str = "https://api.test.profcomff.com/userdata/"
    AUTH_AUTO_ERROR: bool = True
    AUTH_ALLOW_NONE: bool = False
    ENABLE_USERDATA: bool = False
    model_config = ConfigDict(case_sensitive=True, env_file=".env", extra="ignore")


class UnionAuth(SecurityBase):
    model = APIKey.model_construct(in_=APIKeyIn.header, name="Authorization")
    scheme_name = "token"
    settings = UnionAuthSettings()

    def __init__(
        self,
        scopes: list[str] = [],
        auto_error: bool | None = None,
        allow_none: bool | None = None,
        enable_userdata: bool | None = None,
        auth_url=None,  # Для обратной совместимости
        userdata_url=None,
    ) -> None:
        if auth_url is not None:
            warn(
                "auth_url in args deprecated, use AUTH_URL env instead",
                DeprecationWarning,
            )
        if userdata_url is not None:
            warn(
                "userdata_url in args deprecated, use USERDATA_URL env instead",
                DeprecationWarning,
            )
        super().__init__()
        self.auth_url = auth_url or self.settings.AUTH_URL
        if not self.auth_url.endswith("/"):
            self.auth_url = self.auth_url + "/"
        self.userdata_url = userdata_url or self.settings.USERDATA_URL
        if not self.userdata_url.endswith("/"):
            self.userdata_url = self.userdata_url + "/"
        self.auto_error = (
            auto_error if auto_error is not None else self.settings.AUTH_AUTO_ERROR
        )
        self.allow_none = (
            allow_none if allow_none is not None else self.settings.AUTH_ALLOW_NONE
        )
        self.enable_userdata = (
            enable_userdata
            if enable_userdata is not None
            else self.settings.ENABLE_USERDATA
        )
        self.scopes = scopes

    def _except_not_authorized(self):
        if self.auto_error:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Not authorized"
            )
        else:
            return None

    def _except_not_authentificated(self):
        if self.auto_error:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Not authentificated"
            )
        else:
            return None

    async def _get_session(self, token: str | None) -> dict[str, Any] | None:
        if not token and self.allow_none:
            return None
        if not token:
            return self._except_not_authorized()
        return await AsyncAuthLib(auth_url=self.auth_url).check_token(token)

    async def _get_userdata(
        self, token: str | None, user_id: int
    ) -> dict[str, Any] | None:
        if not token and self.allow_none:
            return None
        if not token:
            return self._except_not_authorized()
        if self.enable_userdata:
            return await AsyncAuthLib(userdata_url=self.userdata_url).get_user_data(
                token, user_id
            )
        return None

    async def __call__(
        self,
        request: Request,
    ) -> dict[str, Any] | None:
        token = request.headers.get("Authorization")
        result = await self._get_session(token)
        if result is None:
            return self._except_not_authorized()
        if self.enable_userdata:
            user_data_info = await self._get_userdata(token, result["id"])
            result["userdata"] = []
            if user_data_info is not None:
                result["userdata"] = user_data_info["items"]
        session_scopes = set(
            [scope["name"].lower() for scope in result["session_scopes"]]
        )
        required_scopes = set([scope.lower() for scope in self.scopes])
        if required_scopes - session_scopes:
            self._except_not_authentificated()
        return result
