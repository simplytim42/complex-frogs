install:
	mkdir -p logs
	pip install -r requirements.txt
	playwright install
	playwright install-deps

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
	pytest --cov --cov-report=html .

QA:
	pytest .
	mypy .
	ruff check .

api:
	uvicorn run_api:app --reload

scraper:
	python run_scraper.py