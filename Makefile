configure: venv
	source ./venv/bin/activate && pip install -r requirements.dev.txt -r requirements.txt

venv:
	python3.11 -m venv venv

format:
	source ./venv/bin/activate && autoflake -r --in-place --remove-all-unused-imports ./auth_lib
	source ./venv/bin/activate && isort ./auth_lib
	source ./venv/bin/activate && black ./auth_lib
