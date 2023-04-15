from typing import Any, Final

import pytest
from pytest_mock import mocker

RETURN_VALUE: Final[dict[str, Any]] = {
    "user_id": 0,
    "id": 0,
    "session_scopes": [
        {"id": 0, "name": "userdata.category.create", "comment": ""},
        {"id": 0, "name": "userdata.category.read", "comment": ""},
        {"id": 0, "name": "userdata.category.delete", "comment": ""},
        {"id": 0, "name": "userdata.category.update", "comment": ""},
        {"id": 0, "name": "userdata.param.create", "comment": ""},
        {"id": 0, "name": "userdata.param.read", "comment": ""},
        {"id": 0, "name": "userdata.param.delete", "comment": ""},
        {"id": 0, "name": "userdata.param.update", "comment": ""},
        {"id": 0, "name": "userdata.source.create", "comment": ""},
        {"id": 0, "name": "userdata.source.read", "comment": ""},
        {"id": 0, "name": "userdata.source.delete", "comment": ""},
        {"id": 0, "name": "userdata.source.update", "comment": ""},
        {"id": 0, "name": "userdata.info.read", "comment": ""},
        {"id": 0, "name": "userdata.info.delete", "comment": ""},
        {"id": 0, "name": "userdata.info.update", "comment": ""},
        {"id": 0, "name": "userdata.info.create", "comment": ""},
        {"id": 0, "name": "it.needs.by.test.user.get.first", "comment": ""},
        {"id": 0, "name": "it.needs.by.test.user.get.second", "comment": ""},
        {"id": 0, "name": "it.needs.by.test.user.get.third", "comment": ""},
    ],
    "user_scopes": [
        {"id": 0, "name": "userdata.category.create", "comment": ""},
        {"id": 0, "name": "userdata.category.read", "comment": ""},
        {"id": 0, "name": "userdata.category.delete", "comment": ""},
        {"id": 0, "name": "userdata.category.update", "comment": ""},
        {"id": 0, "name": "userdata.param.create", "comment": ""},
        {"id": 0, "name": "userdata.param.read", "comment": ""},
        {"id": 0, "name": "userdata.param.delete", "comment": ""},
        {"id": 0, "name": "userdata.param.update", "comment": ""},
        {"id": 0, "name": "userdata.source.create", "comment": ""},
        {"id": 0, "name": "userdata.source.read", "comment": ""},
        {"id": 0, "name": "userdata.source.delete", "comment": ""},
        {"id": 0, "name": "userdata.source.update", "comment": ""},
        {"id": 0, "name": "userdata.info.read", "comment": ""},
        {"id": 0, "name": "userdata.info.delete", "comment": ""},
        {"id": 0, "name": "userdata.info.update", "comment": ""},
        {"id": 0, "name": "userdata.info.create", "comment": ""},
    ],
}



@pytest.fixture
def auth_mock(mocker):
    """
    Mock для библиотеки AuthLib, предоставляет все возможные права
    """
    auth_mock = mocker.patch("auth_lib.fastapi.UnionAuth.__call__")
    auth_mock.return_value = RETURN_VALUE
    return auth_mock
