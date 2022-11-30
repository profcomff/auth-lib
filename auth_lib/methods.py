import requests


def email_login(url: str, email: str, password: str) -> dict[str, str]:
    json = {
        "email": email,
        "password": password
    }
    response = requests.post(url=f"{url}/email/login", json=json)
    return response.json()


def check_token(url: str, token: str) -> bool:
    headers = {"Authorization": f"Token {token}"}
    response = requests.post(url=f"{url}/me", headers=headers)
    return True if response.status_code == 200 else False


def logout(url: str, token: str) -> bool:
    headers = {"Authorization": f"Token {token}"}
    response = requests.post(url=f"{url}/logout", headers=headers)
    return True if response.status_code == 200 else False

