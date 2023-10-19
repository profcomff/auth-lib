from auth_lib._methods import AuthAPILib, UserdataAPILib


class AuthLib(AuthAPILib, UserdataAPILib):
    def __init__(self, *, auth_url: str | None = None, userdata_url: str | None = None):
        AuthAPILib.__init__(self, auth_url=auth_url)
        UserdataAPILib.__init__(self, userdata_url=userdata_url)
