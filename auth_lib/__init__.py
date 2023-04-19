try:
    from .testutils import auth_mock
except ImportError:
    print("You have to install 'testing' extras")
    print("pip install 'auth_lib_profcomff[testing]'")