"""Методы аутентификации и авторизации пользователей Airflow API

Документация:
<https://airflow.apache.org/docs/apache-airflow-providers-fab/stable/auth-manager/api-authentication.html>
"""
import os
from typing import Any, Callable
from functools import lru_cache, wraps

from flask import Response, request
from airflow.configuration import conf

from ..methods import AuthLib


API_USER_SCOPE = "airflow.group.apiuser"
DEFAULT_AUTH_URL = "https://api.test.profcomff.com/auth/"
DEFAULT_USERDATA_URL = "https://api.test.profcomff.com/userdata/"
CLIENT_AUTH: tuple[str, str] | Any | None = None  # Требуется Airflow для работы, не удалять


@lru_cache
def get_auth_api() -> AuthLib:
    auth_api = AuthLib(
        auth_url=conf.get("api", "auth_url", fallback=None) or os.getenv("AUTH_URL") or DEFAULT_AUTH_URL,
        userdata_url=conf.get("api", "userdata_url", fallback=None) or os.getenv("USERDATA_URL") or DEFAULT_USERDATA_URL,
    )
    return auth_api


def init_app(_):
    """Инициализация приложения"""


def requires_authentication(fn: Callable):
    """Декоратор для проверки аутентификации

    Все API функции Airflow обернуты в этот декоратор. Функция должна возвращать функцию-обертку,
    проверяющую аутентификацию пользователя
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = get_auth_api().check_token(request.headers.get("Authorization"))
        if user is None:
            return Response("Forbidden", 403)
        if API_USER_SCOPE not in user["session_scopes"]:
            return Response("Unauthorized", 401)
        result = fn(*args, **kwargs)
        return result

    return wrapper
