"""Модуль асинхронных запросов к авторизации

Depricated! Эти функции будут удалены в следующих версиях, используйте синхронный модуль `auth_lib.methods`
"""
import warnings
from typing import Any
from .methods import AuthLib

warnings.warn("Module 'auth_lib.aiomethods' is deprecated", DeprecationWarning)


class AsyncAuthLib:
    auth_url: str
    userdata_url: str

    def __init__(self, *, auth_url: str | None = None, userdata_url: str | None = None):
        warnings.warn("Class 'auth_lib.aiomethods.AsyncAuthLib' is deprecated", DeprecationWarning)
        self.auth_url = auth_url
        self.userdata_url = userdata_url
        self.lib = AuthLib(auth_url=auth_url, userdata_url=userdata_url)

    async def email_login(self, email: str, password: str) -> dict[str, Any]:
        warnings.warn("Method 'auth_lib.aiomethods.AsyncAuthLib.email_login' is deprecated", DeprecationWarning)
        return self.lib.email_login(email, password)

    async def check_token(self, token: str) -> dict[str, Any] | None:
        warnings.warn("Method 'auth_lib.aiomethods.AsyncAuthLib.check_token' is deprecated", DeprecationWarning)
        return self.lib.check_token(token)

    async def logout(self, token: str) -> bool:
        warnings.warn("Method 'auth_lib.aiomethods.AsyncAuthLib.logout' is deprecated", DeprecationWarning)
        return self.lib.logout(token)

    async def get_user_data(self, token: str, user_id: int) -> dict[str | Any] | None:
        warnings.warn("Method 'auth_lib.aiomethods.AsyncAuthLib.get_user_data' is deprecated", DeprecationWarning)
        return self.lib.get_user_data(token, user_id)
