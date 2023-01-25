from abc import ABCMeta, abstractmethod
from typing import Any


class AuthLibMeta(metaclass=ABCMeta):
    url: str

    def __init__(self, url: str):
        self.url = url

    @abstractmethod
    def email_login(self, email: str, password: str) -> dict[str, Any]:
        raise NotImplementedError()

    @abstractmethod
    def check_token(self, token: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def logout(self, token: str) -> bool:
        raise NotImplementedError()