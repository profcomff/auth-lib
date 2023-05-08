try:
    from auth_lib.testing.testutils import auth_mock, pytest_configure
except ImportError as e:
    print("You have to install testing requirements")
    print("pip install 'auth-lib-profcomff[testing]'")
    raise e

__all__ = ["auth_mock", "pytest_configure"]
