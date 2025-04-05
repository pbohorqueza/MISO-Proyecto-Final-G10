# Development Guide for CCP Gestión - Sales Microservice

## Build/Test/Run Commands

### Dependencies Management
- Install dependencies: `uv run sync`
- Activate virtual env (if needed): `source .venv/bin/activate` 

### Running the Application
- Dev server with uv: `uv run -- flask run`
- With Docker: `docker-compose -f compose.dev.yaml up`
- Debug mode: `uv run -- flask run --debug`

### Database Commands
- Create tables: `uv run -- flask db create`
- Seed database: `uv run -- flask db seed`
- Migrations: `uv run -- flask mg [command]` (alias for Flask-Migrate)

### Testing
- Run all tests: `uv run -- pytest`
- Single test: `uv run -- pytest tests/path/to/test_file.py::TestClass::test_method -v`
- With environment variables from .env.test (configured in pytest.ini)

## Code Style Guidelines

### Python
- Use snake_case for variables/functions and PascalCase for classes
- Imports order: standard library → third-party → local (separated by newlines)
- Use explicit error handling with specific exception types
- Use 4-space indentation
- Add type hints for function parameters and return values
- Organize code using Flask blueprints for separation of concerns

### Database Queries
- Use SQLAlchemy 2.0 style for all database operations
- Use `db.session.get(Model, id)` for direct ID lookups
- Use `scalar_one_or_none()` method for safe query execution that returns a single result or None
- Avoid using `Model.query.*` pattern (deprecated in SQLAlchemy 2.0)

### Code Organization
- Follow command pattern for business logic (app/commands/)
- Centralize validation logic in app/lib/validators.py
- Centralize responses in app/responses/**
- Use custom error classes from app/lib/errors.py
- Minimize comments - code should be self-explanatory
- Keep docstrings minimal and focused on "why" not "what"
- Date handling: store as string in YYYY-MM-DD format, validate using validator functions

## Project Structure Notes
- API routes have no prefix - use direct endpoint names (e.g., '/sales-plans')
- Service name in Docker configuration is 'sales'
- Project name in pyproject.toml is 'sales'

