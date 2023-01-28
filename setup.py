from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="auth_lib_profcomff",
    version="0.0.3",
    author="Semyon Grigoriev",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/profcomff/auth-lib",
    packages=find_packages(),
    install_requires=["requests", "aiohttp", "setuptools"],
    extras_require={
        "fastapi": ["fastapi", "starlette"],
    },
    classifiers=[
        "Programming Language :: Python :: 3.11",
    ],
)
