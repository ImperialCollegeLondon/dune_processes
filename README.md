<!-- markdownlint-disable MD041 -->
[![GitHub](https://img.shields.io/github/license/ImperialCollegeLondon/dune_processes)](https://raw.githubusercontent.com/ImperialCollegeLondon/dune_processes/main/LICENSE)
[![Test and build](https://github.com/ImperialCollegeLondon/dune_processes/actions/workflows/ci.yml/badge.svg)](https://github.com/ImperialCollegeLondon/dune_processes/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/ImperialCollegeLondon/dune_processes/graph/badge.svg?token=PG0WTYF8EY)](https://codecov.io/gh/ImperialCollegeLondon/dune_processes)

# DUNE processes web interface

This repo defines the web interface for the DUNE Process Manager.

## For developers

This is a Python application that uses [poetry](https://python-poetry.org) for packaging
and dependency management. It also provides [pre-commit](https://pre-commit.com/) hooks
for various linters and formatters and automated tests using
[pytest](https://pytest.org/) and [GitHub Actions](https://github.com/features/actions).
Pre-commit hooks are automatically kept updated with a dedicated GitHub Action.

To get started:

1. [Download and install Poetry](https://python-poetry.org/docs/#installation) following the instructions for your OS.
1. Clone this repository and make it your working directory
1. Set up the virtual environment:

   ```bash
   poetry install
   ```

1. Activate the virtual environment (alternatively, ensure any Python-related command is preceded by `poetry run`):

   ```bash
   poetry shell
   ```

1. Install the git hooks:

   ```bash
   pre-commit install
   ```

1. Run the main app (this will not receive any data from the drunc process manager):

   ```bash
   python manage.py runserver
   ```

### Running the App

To run this with a demo version of the drunc process manager, run it with docker compose:

```bash
docker compose up -d
```

Dummy processes can be sent to the server with the `scripts/talk_to_process_manager.py` script:

```bash
docker compose exec app python scripts/talk_to_process_manager.py
```

Take the servers down with `docker compose down`

### Development without Docker Compose

In the event that you want to develop without using Docker Compose you must start the
required components manually.

1. Start Kafka - See [Running drunc with pocket kafka].

1. Start the drunc shell:
   `poetry run drunc-unified-shell --log-level debug ./data/process-manager-pocket-kafka.json`

1. Start the application server:
   `poetry run python manage.py runserver`

1. Start the Kafka consumer:
   `poetry run python scripts/kafka_consumer.py`

From here you should be able to see broadcast messages displayed at the top of the index
page on every refresh.

[Running drunc with pocket kafka]: https://github.com/DUNE-DAQ/drunc/wiki/Running-drunc-with-pocket-kafka
