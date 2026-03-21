test:
	@uv run pytest -v test_pyspin.py

lint:
	@uv run ruff check .

create:
	@uv build

upload:
	@uv publish
