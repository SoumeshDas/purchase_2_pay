lint:
	black .
	isort .
	flake8 .

test:
	pytest

format:
	black .
	isort .

ci:
	black --check .
	flake8 .
	pytest