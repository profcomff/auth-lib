from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as readme_file:
    readme = readme_file.read()


with open("requirements.txt", "r", encoding="utf-8") as req_file:
    req = req_file.read().split('\n')


setup(
    name="auth_lib_profcomff",
    version="2023.08.06",
    author="Semyon Grigoriev",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/profcomff/auth-lib",
    packages=find_packages(),
    install_requires=req,
    extras_require={
        "fastapi": ["fastapi", "starlette", "pydantic", "pydantic_settings"],
        "testing": ["pytest"],
    },
    entry_points={"pytest11": ["pytest_auth_lib = auth_lib.testing"]},
    classifiers=[
        "Programming Language :: Python :: 3.11",
    ],
)
