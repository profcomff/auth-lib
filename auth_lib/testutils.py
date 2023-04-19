from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def auth_mock(request):
    marker: pytest.mark = request.node.get_closest_marker("scopes")
    if marker:
        scopes: tuple[str] = marker.args
        session_scopes = []
        for cnt, scope in enumerate(scopes):
            session_scopes.append({"id": cnt, "name": scope, "comment": ""})
        _return_val: dict[str, int | list[dict[str, str | int]]] = {
            "user_id": 0,
            "id": 0,
            "session_scopes": session_scopes,
            "user_scopes": session_scopes,
        }
        patcher = patch(
            "auth_lib.fastapi.UnionAuth.__call__",
            new=MagicMock(return_value=_return_val),
        )
        patcher.start()
        yield
        patcher.stop()
    else:
        return (yield)
