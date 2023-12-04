install:
	mkdir -p logs
	pip install -r requirements.lock
	playwright install
	playwright install-deps

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -rf .coverage

deep-clean: clean
	rm -rf logs/*
	rm -rf htmlcov
	rm -rf frog.db

test-cov:
	pytest --cov --cov-report=html .

QA:
	pytest .
	mypy .
	ruff check .

run:
	python main.py