import warnings
from typing import Optional, Any

from fastapi import HTTPException, Header
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED
from typing import Callable, Awaitable
from functools import wraps
import asyncio


class OAuth2TokenAPI(OAuth2):
    def __init__(
        self,
        authorizationUrl: str,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[dict[str, str]] = None,
        description: Optional[str] = None,
        refreshUrl: Optional[str] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}

        flows = OAuthFlowsModel(
            authorizationCode={
                "authorizationUrl": authorizationUrl,
                "tokenUrl": tokenUrl,
                "refreshUrl": refreshUrl,
                "scopes": scopes,
            }
        )
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        authorization = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "token":
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Token"},
                )
            else:
                return None
        return param


def auth_required(url: str):
    def _auth_required(endpoint: Callable[[object], Awaitable[object]]):
        async def auth_endpoint(*args, request: Request, authorization: str = Header(...), **kwargs) -> object:
            scheme, param = get_authorization_scheme_param(authorization)
            if not authorization or scheme.lower() != "token":
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Token"},
                )
            from .methods import check_token
            check = check_token(url, param)
            if not check:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Token"},
                )
            return await endpoint(*args, **kwargs)

        import inspect
        auth_endpoint.__signature__ = inspect.Signature(
            parameters=[
                # Use all parameters from handler
                *inspect.signature(endpoint).parameters.values(),

                # Skip *args and **kwargs from wrapper parameters:
                *filter(
                    lambda p: p.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD),
                    inspect.signature(auth_endpoint).parameters.values()
                )
            ],
            return_annotation=inspect.signature(endpoint).return_annotation,
        )
        return auth_endpoint
    return _auth_required



