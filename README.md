# complex-frogs
web scraping to track the price of things I would like to buy and send me daily notifications using https://pushover.net

there are two main scripts, the first is the scraper that collects the data. The second is the API which enables user interaction with the data.

NOTE: This project is intended to be deployed on a RaspberryPi and thus this README assumes such.

## setup
1. sign up to https://pushover.net and generate an API TOKEN and a USER KEY.
1. clone repo and `cd` into it
1. `python -m venv venv`
1. `source venv/bin/activate`
1. rename `.env-example` to `.env` and populate the variables with your API TOKEN and USER KEY.
1. `make install` (or `make dev-install` for local development)

### deploy locally
1. to execute the scraper use the command `make scraper`
1. to activate the API use `make api`

### deploy to RPI
1. setup a cronjob to run the scraper once a day
1. update the following variables in the systemd service file to represent the RPI environment:
    - ExecStart
    - WorkingDirectory
    - User
    - Group
1. `cp` the file into the `/etc/systemd/system` directory
1. run `sudo systemctl enable complex-frogs` to set the script to boot on startup
1. run `sudo systemctl start complex-frogs` to start the script now (without having to reboot)


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