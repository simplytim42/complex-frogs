install:
	mkdir -p logs
	pip install -r requirements.txt
	playwright install
	playwright install-deps

	# run the scraper once to create the database
	python run_scraper.py

dev-install: install
	pip install -r requirements-dev.txt

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -rf .coverage

deep-clean: clean
	rm -rf logs/*
	rm -rf htmlcov
	rm -rf frog.db

test-cov:
	pytest --cov=complex_frogs --cov-report=html .

QA:
	pytest .
	mypy .
	ruff check .
