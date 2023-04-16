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
        {"id": 0, "name": "timetable.lecturer.create", "comment": ""},
        {"id": 0, "name": "timetable.lecturer.update", "comment": ""},
        {"id": 0, "name": "timetable.lecturer.delete", "comment": ""},
        {"id": 0, "name": "timetable.lecturer.read", "comment": ""},
        {"id": 0, "name": "timetable.room.create", "comment": ""},
        {"id": 0, "name": "timetable.room.update", "comment": ""},
        {"id": 0, "name": "timetable.room.delete", "comment": ""},
        {"id": 0, "name": "timetable.room.read", "comment": ""},
        {"id": 0, "name": "timetable.group.create", "comment": ""},
        {"id": 0, "name": "timetable.group.read", "comment": ""},
        {"id": 0, "name": "timetable.group.delete", "comment": ""},
        {"id": 0, "name": "timetable.group.update", "comment": ""},
        {"id": 0, "name": "timetable.lecturer.comment.review", "comment": ""},
        {"id": 0, "name": "timetable.lecturer.photo.review", "comment": ""},
        {"id": 0, "name": "timetable.event.comment.review", "comment": ""},
        {"id": 0, "name": "services.category.create", "comment": ""},
        {"id": 0, "name": "services.category.update", "comment": ""},
        {"id": 0, "name": "services.category.delete", "comment": ""},
        {"id": 0, "name": "services.button.create", "comment": ""},
        {"id": 0, "name": "services.button.update", "comment": ""},
        {"id": 0, "name": "services.button.delete", "comment": ""},
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
        {"id": 0, "name": "it.needs.by.test.user.get.first", "comment": ""},
        {"id": 0, "name": "it.needs.by.test.user.get.second", "comment": ""},
        {"id": 0, "name": "it.needs.by.test.user.get.third", "comment": ""},
        {"id": 0, "name": "timetable.lecturer.create", "comment": ""},
        {"id": 0, "name": "timetable.lecturer.update", "comment": ""},
        {"id": 0, "name": "timetable.lecturer.delete", "comment": ""},
        {"id": 0, "name": "timetable.lecturer.read", "comment": ""},
        {"id": 0, "name": "timetable.room.create", "comment": ""},
        {"id": 0, "name": "timetable.room.update", "comment": ""},
        {"id": 0, "name": "timetable.room.delete", "comment": ""},
        {"id": 0, "name": "timetable.room.read", "comment": ""},
        {"id": 0, "name": "timetable.group.create", "comment": ""},
        {"id": 0, "name": "timetable.group.read", "comment": ""},
        {"id": 0, "name": "timetable.group.delete", "comment": ""},
        {"id": 0, "name": "timetable.group.update", "comment": ""},
        {"id": 0, "name": "timetable.lecturer.comment.review", "comment": ""},
        {"id": 0, "name": "timetable.lecturer.photo.review", "comment": ""},
        {"id": 0, "name": "timetable.event.comment.review", "comment": ""},
        {"id": 0, "name": "services.category.create", "comment": ""},
        {"id": 0, "name": "services.category.update", "comment": ""},
        {"id": 0, "name": "services.category.delete", "comment": ""},
        {"id": 0, "name": "services.button.create", "comment": ""},
        {"id": 0, "name": "services.button.update", "comment": ""},
        {"id": 0, "name": "services.button.delete", "comment": ""},
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
