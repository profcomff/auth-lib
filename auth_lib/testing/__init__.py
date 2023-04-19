try:
    from auth_lib.testing.testutils import auth_mock, pytest_configure
except ImportError:
    print("You have to install testing requirements")
    print("pip install 'auth-lib-profcomff[testing]'")
