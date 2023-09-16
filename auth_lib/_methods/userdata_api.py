from typing import Any
from urllib.parse import urljoin

import requests


class UserdataAPILib:
    userdata_url: str

    def __init__(self, *, userdata_url: str | None = None):
        self.userdata_url = userdata_url

    def get_user_data(self, token: str, user_id: int) -> dict[str | Any] | None:
        headers = {"Authorization": token}
        response = requests.get(
            url=urljoin(self.userdata_url, f"user/{user_id}"), headers=headers
        )
        if response.ok:
            return response.json()
        return None
