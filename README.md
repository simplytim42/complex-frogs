# complex-frogs
web scraping to track the price of things I would like to buy and send me daily notifications using https://pushover.net

# setup
1. sign up to https://pushover.net and generate an API TOKEN and a USER KEY.
1. `python -m venv venv`
1. `source venv/bin/activate`
1. `pip install -r requirements.txt`
1. rename `.env-example` to `.env` and populate the variables with your API TOKEN and USER KEY.
1. inside the `data` direcory, rename `scraping_data.example.json` to `scraping_data.json` and populate the relevant scraping data.
1. `python main.py`
