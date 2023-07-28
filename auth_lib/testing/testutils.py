from unittest.mock import AsyncMock, patch

import pytest


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "authenticated(*scopes): mark test to mock auth_lib"
    )


@pytest.fixture(autouse=True)
def auth_mock(request):
    marker: pytest.mark = request.node.get_closest_marker("authenticated")
    if not marker:
        return (yield)
    scopes: tuple[str] = marker.args
    session_scopes = []
    for cnt, scope in enumerate(scopes):
        session_scopes.append({"id": cnt, "name": scope, "comment": ""})
    _return_val: dict[str, int | list[dict[str, str | int]]] = {
        "id": marker.kwargs.get("user_id", 0),
        "session_scopes": session_scopes,
        "user_scopes": session_scopes,
    }
    patcher = patch(
        "auth_lib.fastapi.UnionAuth._get_session",
        new=AsyncMock(return_value=_return_val),
    )
    patcher.start()
    yield
    patcher.stop()
