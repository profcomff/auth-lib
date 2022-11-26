import aiohttp


async def email_login(url: str, email: str, password: str) -> dict[str, str]:
    json = {
        "email": email,
        "password": password
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"{url}/email/login", json=json) as response:
            return await response.json()


async def check_token(url: str, token: str) -> bool:
    headers = {"Authorization": f"Token {token}"}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url=f"{url}/me") as response:
            return True if response.status == 200 else False


async def logout(url: str, token: str) -> bool:
    headers = {"Authorization": f"Token {token}"}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url=f"{url}/logout") as response:
            return True if response.status == 200 else False

