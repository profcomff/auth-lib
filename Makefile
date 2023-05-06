configure: venv
	source ./venv/bin/activate && pip install -r requirements.dev.txt

venv:
	python3.11 -m venv venv

format:
	autoflake -r --in-place --remove-all-unused-imports ./auth_lib
	isort ./auth_lib
	black ./auth_lib


