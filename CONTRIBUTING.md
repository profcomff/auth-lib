## Что нужно для запуска 

 1. python3.11. Установка описана [тут](https://www.python.org/downloads/)

 2. Завсимости, описанные в setup.py, requirements.dev.txt

## Как тестировать при разработке
1. Создаете ветку в репозитории, разрабатываете там
2. Закончили - коммитите изменения
3. Заходите в любой fastapi проект
4. Установите вашу версию. Вот как это сделать: https://stackoverflow.com/questions/20101834/pip-install-from-git-repo-branch
5. Тестируйте все методы из methods.py, aiomethods.py, UnionAuth.__call__()

## Как контрибьютить
1. `git clone https://github.com/profcomff/auth-lib.git`
2. Создавайте ветку
### Если хотите добавить новый общий метод
3. Написать этот метод в файл /auth_lib/methods.py - синхронная версия и, если есть возможность, в файл /auth_lib/aiomethods/py - асинхронная версия
4. Протестировать метод на локальном/тестовом АПИ
### Если хотите добавить логику в общий класс порверки аутентификации и авторизации 
3. Прочитайте как работает Depends: https://fastapi.tiangolo.com/tutorial/dependencies/
4. Нужная вам логика описана в /auth_lib/fastapi.py. Основной метод - __call__.py.
### Если хотите поменять логику тестирования библиотеки 
3. Прорчитайте про используемые в этой библиотеке [моки](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch) из unittest
4. Прочитайте про [pytest fixtures](https://docs.pytest.org/en/6.2.x/fixture.html#what-fixtures-are). [Это](https://habr.com/ru/articles/448786/) тоже неплохая статья.
5. Нужная вам логика описана в /auth_lib/testing/testutils.py.

## Codestyle

 - Black. Как пользоваться описано [тут](https://black.readthedocs.io/en/stable/)

 - Также применяем [isort](https://pycqa.github.io/isort/)
