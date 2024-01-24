# CHANGELOG

# V-TBD
- Add a `CHANGELOG` file and backdate it
- Rename `get_test_db` and update it to follow `fastapi` docs examples
- Update DELETE endpoints to return the data that has been deleted

# V2.2.0
- Update the name of the project throughout the repo to "Intrepid"

# V2.1.0
- Improve documentation and add license
- Add API tests for targets and scrape data endpoints
- Rename `complex_frogs` dir to `src`
- Exclude `repr` functions from coverage and config test to ignore `NotImplementedErrors`
- Refactor test files and exception handling for API endpoints
- Refactor API messages and update error handling

## V2.0.0: The First Breaking Change Release (ish)
### Breaking Changes
As far as breaking changes go these are pretty minor. Management of API endpoints was modularised and as a result some of the endpoints now require a trailing `/`.

- Create DB CRUD functions
- Improve API functionality and session management
- Add unit tests for CRUD functions and improve model tests
- Raise error if no price or title found
- Split API endpoints into separate routers
- Add service file for auto startup of API

## V1.3.0: The API Release
- Encapsulate the logging configuration & split dependencies into prod and dev
- Move functions into their own utils modules
- Move tests into file structure mirroring complex_frogs
- Add API endpoint for reading the scraping targets
- Add API endpoint for creating new scraping targets
- Add API endpoint for updating scraping targets
- Add API endpoint for deleting scraping targets
- Add API endpoint for reading scraping data
- Add API endpoint for deleting scraping data

## V1.2.0
- Implement DB
- Clean old DB
- Ensure DB creation happens during import for new projects
- Manage requirements with a lock file
- Add Makefile to trigger common tasks
- Ensure log file is in an appropriate location
- Manage package imports within `init.py`
- Use time zone aware UTC objects
- Configure Ruff and implement corrections
- Combine GitHub actions into single CI file and collect all custom modules into a `complex_frogs` directory

## V1.1.0
This is part 1 of migrating to a SQLite database. This release provides a migration script and the dependencies that can convert an existing installation to rely on sqlite.

## V1.0.0: The Web Scraper Release
- Add tests
- Add static analysis
- Add CI workflow
- Fix Ruff & Mypy results
- Improve unit testing coverage
- Get classes to use their `repr` when logging
- Refactor
- Initial scraper codebase
