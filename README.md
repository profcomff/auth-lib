# auth-lib
Библиотека функций авторизации для микросервисов Твой ФФ!


## Примеры использования
```python
from auth_lib.fastapi import UnionAuth

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
