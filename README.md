# complex-frogs
web scraping to track the price of things I would like to buy and send me daily notifications using https://pushover.net

## setup
1. sign up to https://pushover.net and generate an API TOKEN and a USER KEY.
1. `python -m venv venv`
1. `source venv/bin/activate`
1. rename `.env-example` to `.env` and populate the variables with your API TOKEN and USER KEY.
1. `make install` (or `make dev-install` for local development)
1. `make run`

## run all QA checks
1. `make QA`

## run tests
1. open a terminal and ensure you are in the project's root dir
1. `pytest .`

## run test coverage
1. open a terminal and ensure you are in the project's root dir
1. `pytest --cov .` will produce an overview report in the cli
1. `make test-cov` will produce html reports in a `htmlcov` directory

## code quality checks
1. open a terminal and ensure you are in the project's root dir
1. `ruff check .` will run the code linter
1. `mypy .` will run the type checker

## remove cache files
1. `make clean`

## remove cache files, logs and db (fresh start for dev)
1. `make deep-clean`