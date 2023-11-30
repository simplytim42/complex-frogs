install:
	pip install -r requirements.lock
	playwright install
	playwright install-deps

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf .mypy_cache
	rm -rf .ruff_cache

deep-clean: clean
	rm -rf htmlcov
	rm -rf html_logs
	rm -rf frog.log
	rm -rf frog.db

test-cov:
	pytest --cov --cov-config=.coveragerc --cov-report=html .

QA:
	pytest .
	mypy .
	ruff check .

run:
	python main.py