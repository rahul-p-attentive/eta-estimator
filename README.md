# ETA Estimator

A Django project with PostgreSQL database.

## Prerequisites

- Python 3.9 or higher
- Poetry (Python package manager)
- PostgreSQL

## Setup

1. Install Poetry if you haven't already:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Create a PostgreSQL database:
   ```bash
   createdb eta_estimator
   ```

4. Copy `.env.example` to `.env` and update the values:
   ```bash
   cp .env.example .env
   ```

5. Run migrations:
   ```bash
   poetry run python manage.py migrate
   ```

6. Start the development server:
   ```bash
   poetry run python manage.py runserver
   ```

## Development

- Run tests: `poetry run pytest`
- Format code: `poetry run black .`
- Lint code: `poetry run flake8`

## Project Structure

```
eta-estimator/
├── manage.py
├── pyproject.toml
├── requirements.txt
├── .env.example
└── eta_estimator/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```