# auth-lib
Библиотека функций авторизации для микросервисов Твой ФФ!


## Примеры использования
```python
from auth_lib.fastapi import UnionAuth
from fastapi import APIRouter, Depends
router = APIRouter(prefix="/...")

## Чтобы дернуть ручку нужен один скоуп, авторизация обязательна
## Юзкейс https://github.com/profcomff/timetable-api/blob/a374c74cd960941100f6c923ff9c3ff706a1ed09/calendar_backend/routes/room/room.py#L45
@router.smth("/")
async def foo(_=Depends(UnionAuth(scopes=["service.resource.method"], allow_none=False, auto_error=True))):
  pass
  
## Чтобы дернуть ручку нужно два скоупа, авторизация обязательна
## Юзкейс https://github.com/profcomff/print-api/blob/775f36fdd185eec8d9096d3472b7730cf5ac9798/print_service/routes/user.py#L78
@router.smth("/")
async def bar(_=Depends(UnionAuth(scopes=["scope1", "scope2"], allow_none=False, auto_error=True))):
  pass
  
## Чтобы дернуть ручку не нужны скоупы, авторизация необязательна, но если передана недействительная сессия, то кинет ошибку
@router.smth("/")
async def baz(_=Depends(UnionAuth(scopes=[], allow_none=True, auto_error=True))):
  pass


## Чтобы дернуть ручку не нужны скоупы, авторизация обязательна
@router.smth("/")
async def foo(_=Depends(UnionAuth(scopes=[], allow_none=False, auto_error=True))):
  pass

```
Depends вызывает инстанс класса с нужными параметрами и возвращает словарь со всеми полями отсюда https://api.test.profcomff.com/#/Logout/me_me_get

Описание класса UnionAuth
Поля
```
scopes: list[str] - список имен скоупов, которые нужны в данной ручке. Например ["printer.user.create", "printer.user.delete"]
allow_none: bool - Если true, то при отсутствии нужного заголовка в запросе ручка будет доступна юзеру, если заголовк передан, то обработка идет в зависимости от следующего параметра
auto_error: bool - если true, то при несовпадении скоупов/завершенной сессии и тд(на запрос GET /me не 200) - кинет 401, если false, то не будет кидать ошибки, но будет возвращать None
```
Чтобы задать хост авторизации надо в переменные окружения или в .env файл прописать AUTH_URL="..."

Defaults 
```python
auth_url="https://api.test.profcomff.com/auth/"
AUTH_AUTO_ERROR: bool = True
AUTH_ALLOW_NONE: bool = False

```

Пример мока библиотеки:

Установите нужные завивсимости
```shell
pip install 'auth-lib-profcomff[testing]'
```

```python
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

@pytest.fixture
def client(auth_mock):
    yield TestClient(FastAPI())

@pytest.mark.authenticated("scope1", "scope2", ...)
def test1(client): ## В этом тесте будут выданы скоупы scope1, scope2,
    # библиотека не будет проверять токен через АПИ, будет просто возвращать
    # нужный словарь, как будто пользователь авторизован с нужными скоупами
    assert 2*2 == 4

    
@pytest.mark.authenticated()
def test2(client): ## В этом тесте скоупов выдано не будет,
    # но библиотека не будет проверять токен через АПИ, будет просто возвращать
    # нужный словарь, как будто пользователь авторизован с нужными скоупами
    assert 2*2 == 4


def test3(client): ## В этом тесте скоупов выдано не будет, библиотека будет проверять 
    # токен через АПИ
    assert 2*2 == 4
```
