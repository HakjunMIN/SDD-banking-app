# Banking App Backend

FastAPI backend service for the Banking App transaction history feature.

## Setup

This project uses [uv](https://github.com/astral-sh/uv) for Python package management.

### Prerequisites

- Python 3.11+
- uv package manager

### Installation
s
1. Install dependencies:
   ```bash
   uv sync
   ```

2. Install development dependencies:
   ```bash
   uv sync --dev
   ```

### Running the Application

1. Start the development server:
   ```bash
   uv run uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
   ```

2. Open your browser to [http://localhost:8000](http://localhost:8000)

3. Access API documentation:
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Development

1. Run tests:
   ```bash
   uv run pytest
   ```

2. Code formatting:
   ```bash
   uv run black src/
   uv run isort src/
   ```

3. Type checking:
   ```bash
   uv run mypy src/
   ```

4. Linting:
   ```bash
   uv run flake8 src/
   ```

## Project Structure

```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py           # FastAPI application entry point
│   ├── config.py         # Application configuration
│   ├── database/         # Database connection and models
│   ├── models/           # Pydantic models and schemas
│   └── routers/          # API endpoint routers
├── tests/                # Test files
├── pyproject.toml        # Project configuration and dependencies
└── README.md            # This file
```

## API Endpoints

- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

Additional endpoints will be added for transaction history features.