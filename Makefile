yapf:
	poetry run yapf --recursive -i .

pylint:
	poetry run pylint digester

test:
	poetry run pytest --cov digester --cov-report html:.cov --cov-report term

check: yapf pylint test

job: poetry run python -m digester.job
