# dune_processes

This repo defines the web app for the Dune Process Manager web interface.

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

_Note that this depends on a very large docker base image._

To run this with a demo version of the drunc process manager, run it with docker compose:

```bash
docker compose up -d
```

Dummy processes can be sent to the server with the `scripts/talk_to_process_manager.py` script:

```bash
docker compose exec app python scripts/talk_to_process_manager.py
```

To boot a more realistic test session:

```bash
docker compose exec drunc bash -c "source env.sh && drunc-process-manager-shell grpc://localhost:10054 boot test/config/test-session.data.xml test-session"
```

_Note that the above consumes several Gb of memory._

Once booted you can interact with the root controller via:

```bash
docker compose exec drunc bash -c "source env.sh && drunc-controller-shell grpc://localhost:3333"
```

For details of working with the controller see the [drunc wiki].

Take the servers down with `docker compose down`.

[drunc wiki]: https://github.com/DUNE-DAQ/drunc/wiki/Controller
