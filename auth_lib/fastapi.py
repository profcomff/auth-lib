from typing import Callable, Awaitable

from fastapi import HTTPException, Header
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED


def auth_required(url: str):
    def _auth_required(endpoint: Callable[[object], Awaitable[object]]):
        async def auth_endpoint(request: Request, *args, authorization: str = Header(...), **kwargs) -> object:
            if not request.headers.get("authorization"):
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Token"},
                )
            from .methods import check_token
            check = check_token(url, authorization)
            if not check:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Auth error",
                    headers={"WWW-Authenticate": "Token"},
                )
            return await endpoint(*args, **kwargs)

        import inspect
        auth_endpoint.__signature__ = inspect.Signature(
            parameters=[
                *inspect.signature(endpoint).parameters.values(),

                *filter(
                    lambda p: p.kind not in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD),
                    inspect.signature(auth_endpoint).parameters.values()
                )
            ],
            return_annotation=inspect.signature(endpoint).return_annotation,
        )
        return auth_endpoint
    return _auth_required



