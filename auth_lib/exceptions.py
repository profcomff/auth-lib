class AuthError(Exception):
    """Базовая ошибка библиотеки auth-lib"""


class IncorrectData(AuthError):
    def __init__(self, response: dict):
        super().__init__(str(response))


class AuthFailed(AuthError):
    def __init__(self, response: dict):
        super().__init__(str(response))


class SessionExpired(AuthError):
    def __init__(self, response: dict):
        super().__init__(str(response))


class NotFound(AuthError):
    def __init__(self, response: dict):
        super().__init__(str(response))
