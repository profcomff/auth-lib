from auth_lib.aiomethods import AsyncAuthAPILib, AsyncUserdataAPILib


class AsyncAuthLib(AsyncAuthAPILib, AsyncUserdataAPILib):
    def __init__(self, *, auth_url: str | None = None, userdata_url: str | None = None):
        AsyncAuthAPILib.__init__(self, auth_url=auth_url)
        AsyncUserdataAPILib.__init__(self, userdata_url=userdata_url)
