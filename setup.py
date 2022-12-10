from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

with open("requirements.txt", "r") as req_file:
    req = req_file.read().splitlines()


setup(
    name="auth_lib",
    version="0.0.1",
    author="Semyon Grigoriev",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/profcomff/auth-lib",
    packages=find_packages(),
    install_requires=req,
    classifiers=[
        "Programming Language :: Python :: 3.11",
    ],
)