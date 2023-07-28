from setuptools import find_packages, setup

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="auth_lib_profcomff",
    version="2023.07.28",
    author="Semyon Grigoriev",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/profcomff/auth-lib",
    packages=find_packages(),
    install_requires=["requests", "aiohttp", "setuptools"],
    extras_require={
        "fastapi": ["fastapi", "starlette", "pydantic", "pydantic_settings"],
        "testing": ["pytest"],
    },
    entry_points={"pytest11": ["pytest_auth_lib = auth_lib.testing"]},
    classifiers=[
        "Programming Language :: Python :: 3.11",
    ],
)
