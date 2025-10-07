# XU-News-AI-RAG Backend

This directory contains the Flask backend for the XU-News-AI-RAG project. It provides a RESTful API for user authentication, knowledge base management, AI-powered search, and data analysis.

## Prerequisites

- [uv](https://github.com/astral-sh/uv)
- Python 3.11

## Setup

1.  **Install Dependencies:**
    Use `uv` to install the required packages from `pyproject.toml` and `uv.lock`.

    ```bash
    uv sync
    ```

2.  **Configure Environment:**
    Create a `.env` file from the example and update it with your specific configuration, such as database URI, JWT secret key, and the URLs for your `llama-server` instance.

    ```bash
    cp .env.example .env
    ```

## Running the Server

You can run the backend server using `uv` with a production-ready WSGI server like Gunicorn.

```bash
uv run gunicorn "backend.app:create_app()"
```

The server will start on `http://127.0.0.1:8000` by default.

## Running Tests

The test suite uses `pytest`. To run the tests, execute the following command from the `backend` directory:

```bash
uv run -m pytest
```

To generate a coverage report:

```bash
uv run -m pytest --cov
```
