<!-- markdownlint-disable MD041 -->
[![GitHub](https://img.shields.io/github/license/ImperialCollegeLondon/drunc_ui)](https://raw.githubusercontent.com/ImperialCollegeLondon/drunc_ui/main/LICENSE)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/ImperialCollegeLondon/drunc_ui/main.svg)](https://results.pre-commit.ci/latest/github/ImperialCollegeLondon/drunc_ui/main)
[![Test and build](https://github.com/ImperialCollegeLondon/drunc_ui/actions/workflows/ci.yml/badge.svg)](https://github.com/ImperialCollegeLondon/drunc_ui/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/ImperialCollegeLondon/drunc_ui/graph/badge.svg?token=PG0WTYF8EY)](https://codecov.io/gh/ImperialCollegeLondon/drunc_ui)

# DUNE Run Control User Interface (drunc-ui)

This repo defines the web interface for the DUNE Process Manager.

## Running the App

To run with a demo version of the drunc process manager, run it with docker compose:

```bash
docker compose up
```

It can take a few moment for the services to boot but the application should then be
available in the browser at <http://localhost:8000>.  Authentication is required to work
with the application so you need to create a user account to work with:

```bash
docker compose exec app python manage.py createsuperuser
```

and follow the prompts. You should then be able to use the details you supplied to pass
the login screen. You can use the "boot" button on the main page to create simple
processes to experiment with. You can also do this via the command line:

```bash
docker compose exec app python scripts/talk_to_process_manager.py
```

Take the services down with `docker compose down` or by pressing Ctrl+C in the
corresponding terminal.

## Development

Working with the full functionality of the web application requires a number of services
to be started and to work in concert. The Docker Compose stack provides the required
services and is suitable for development and manual testing but is not suitable for
running QA (pre-commit) tooling or unit tests. The project directory is mounted into the
`app` service which allows the Django development server's auto-reload mechanism to
detect changes to local files and work as expected.

It is recommended that you follow the below instructions on working with poetry to run
the project's QA tooling and Unit Tests.

### Working with Poetry

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

Pre-commit should now work as expected when making commits even without the need to have
an active poetry shell. You can also manually run pre-commit (e.g. `pre-commit run -a`)
and the unit tests with `pytest`. Remember you'll need to prefix these with `poetry run`
first if you don't have an active poetry shell.

#### Running the web application with Poetry

You can also start the web application though at a minimum this requires the drunc
process manager to be running. Note that drunc only works on Linux so this approach will
not work on any other platforms. See the next section on also working with
Kafka. Assuming you have an active poetry shell for all steps:

1. Start the drunc shell:

   ```bash
   drunc-unified-shell --log-level debug ./data/process-manager-no-kafka.json
   ```

1. In another terminal, run the main app:

   ```bash
   python manage.py runserver
   ```

1. As above you'll need to create a user to get past the login page:

   ```bash
   python manage.py createsuperuser
   ```

Note that if you boot any processes in the web application this will immediately die
with an exit code of 255. This is because the drunc shell requires an ssh server on
localhost in order to be able to run processes. In most cases this isn't very limiting.

#### Running the web application with Poetry and Kafka

In the event that you want to work with the full application without using Docker
Compose you must start the required components manually. Assuming you have an active
poetry shell for all steps.

1. Start Kafka - See [Running drunc with pocket kafka].

1. Start the drunc shell:
   `drunc-unified-shell --log-level debug ./data/process-manager-pocket-kafka.json`

1. Start the application server:
   `python manage.py runserver`

1. Start the Kafka consumer:
   `python manage.py kafka_consumer --debug`

From here you should be able to see broadcast messages displayed at the top of the index
page on every refresh.

[Running drunc with pocket kafka]: https://github.com/DUNE-DAQ/drunc/wiki/Running-drunc-with-pocket-kafka
