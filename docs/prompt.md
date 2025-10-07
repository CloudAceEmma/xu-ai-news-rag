# Prompt for Building the XU-News-AI-RAG Backend

You are an expert software engineering AI agent. Your task is to create the complete backend for the XU-News-AI-RAG project based on the provided documentation (`PRD.md`, `uv.md`, `llama-server.md`).

Your implementation must be a Flask application managed with `uv`, adhering to the architecture and features described.

## 1. Core Requirements & Constraints

- **Technology Stack:** Use Python 3.11, Flask, SQLAlchemy, Flask-JWT-Extended, and `uv` for package management as specified in the documentation.
- **AI Models & API Endpoints (Crucial):** The implementation must use the exact models and `llama-server` HTTP endpoints specified below. Do not deviate. The base URLs for these services will be provided via environment variables.
    - **LLM:**
        - **Model:** `ggml-org/Qwen3-1.7B-GGUF`
        - **Endpoint:** `POST /v1/chat/completions`
    - **Embedding Model:**
        - **Model:** `ggml-org/embeddinggemma-300M-GGUF`
        - **Endpoint:** `POST /v1/embeddings`
    - **Reranking Model:**
        - **Model:** `gpustack/bge-reranker-v2-m3-GGUF`
        - **Endpoint:** `POST /rerank`
- **Database:** Use SQLite for metadata and FAISS for vector storage, with a separate FAISS index for each user.
- **Testing:** You must write a comprehensive test suite using `pytest` that covers all API endpoints and services, achieving at least 80% code coverage.

## 2. Project Structure

Organize the backend project with the following directory structure:

```
backend/
├── .env.example
├── .python-version
├── pyproject.toml
├── src/
│   └── backend/
│       ├── __init__.py
│       ├── app.py
│       ├── config.py
│       ├── models.py
│       ├── auth/
│       │   ├── __init__.py
│       │   └── routes.py
│       ├── routes/
│       │   ├── __init__.py
│       │   └── main.py
│       └── services/
│           ├── __init__.py
│           ├── aggregation.py
│           ├── clustering.py
│           ├── custom_cross_encoder.py
│           ├── custom_llm.py
│           ├── feeds.py
│           ├── knowledge_base.py
│           ├── notification.py
│           └── search.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_aggregation.py
    ├── test_auth.py
    ├── test_clustering.py
    ├── test_documents.py
    ├── test_feeds.py
    ├── test_reports.py
    ├── test_search.py
    └── testdata/
        └── rss.xml
```

## 3. Step-by-Step Implementation Guide

### Step 1: Setup and Configuration

1.  **`pyproject.toml`**: Define all project dependencies as listed in the existing `pyproject.toml` file. Add a `[tool.pytest.ini_options]` section to set the `pythonpath` to `src`. Also add a `[tool.coverage.run]` section to source from `src`.
2.  **`.env.example`**: Create an example environment file containing all necessary configuration variables (Flask keys, database URI, Llama server URLs, etc.).
3.  **`config.py`**: Implement a `Config` class to load these environment variables.

### Step 2: Database Models (`models.py`)

Define the SQLAlchemy models as described in the technical architecture:
-   `User`: Must include `id`, `username`, and `password_hash`, with methods for setting and checking the password.
-   `Document`: Must include fields for `user_id` (foreign key), `file_path`, `document_type`, `source`, `tags`, and `uploaded_at`.
-   `RssFeed`: Must include `user_id` (foreign key) and `url`.

### Step 3: Authentication (`auth/routes.py`)

-   Create a Flask Blueprint for authentication.
-   Implement the `/register` endpoint to create a new user.
-   Implement the `/login` endpoint to authenticate a user and return a JWT access token.

### Step 4: Core Services (`services/`)

This is the core logic of the application.

1.  **`custom_llm.py`**: Create a custom LangChain LLM class `LlamaServerLLM` that makes a POST request to the `/v1/chat/completions` endpoint of the `llama-server`. It must use the `ggml-org/Qwen3-1.7B-GGUF` model.
2.  **`search.py` (Embedding Class)**: Inside this file, create a custom LangChain Embeddings class `LlamaServerEmbeddings`. It must implement `embed_documents` and `embed_query` by making POST requests to the `/v1/embeddings` endpoint of the `llama-server`, specifying the `ggml-org/embeddinggemma-300M-GGUF` model.
3.  **`custom_cross_encoder.py`**: Create a custom LangChain `BaseCrossEncoder` class `LlamaServerCrossEncoder` that makes a POST request to the `/rerank` endpoint of the `llama-server`, specifying the `gpustack/bge-reranker-v2-m3-GGUF` model.
4.  **`knowledge_base.py`**:
    -   Implement logic to handle file uploads (TXT, PDF, XLSX).
    -   Use the appropriate LangChain `DocumentLoader` for each file type.
    -   Use `RecursiveCharacterTextSplitter` to chunk the documents.
    -   Use the `LlamaServerEmbeddings` class to create vector embeddings.
    -   Store the embeddings in a user-specific FAISS index (`faiss_index/user_<id>`).
    -   Implement functions for document deletion (single and batch) and metadata editing.
5.  **`search.py` (Search Logic)**:
    -   Implement the `perform_search` function which orchestrates the RAG pipeline.
    -   It should load the user's FAISS index and create a retriever.
    -   Use `ContextualCompressionRetriever` with the `LlamaServerCrossEncoder` to rerank results.
    -   Construct a `RetrievalQA` chain using the `LlamaServerLLM`.
    -   Implement the fallback logic to call `_bing_search` if no documents are found in the local index.
    -   Implement `generate_keyword_report` to calculate and return the top 10 keywords.
6.  **`aggregation.py`**: Implement `run_aggregation_for_all_users` to fetch articles from all user-subscribed RSS feeds, extract content, and add them to the knowledge base using the `add_document` function.
7.  **`clustering.py`**: Implement `generate_cluster_report` using `TfidfVectorizer` and `KMeans` from scikit-learn to cluster documents and return the top terms for each cluster.
8.  **`notification.py`**: Implement a `send_notification` function using `Flask-Mail`.

### Step 5: API Endpoints (`routes/main.py`)

-   Create a main Flask Blueprint.
-   Protect all endpoints with `@jwt_required()`.
-   Create endpoints that map to the features in the PRD, calling the appropriate service functions:
    -   `GET /documents`: List and filter documents.
    -   `POST /documents`: Upload a document.
    -   `DELETE /documents/<int:doc_id>`: Delete a document.
    -   `POST /documents/batch_delete`: Delete multiple documents.
    -   `PUT /documents/<int:doc_id>`: Edit document metadata.
    -   `POST /search`: Perform a search query.
    -   `GET /report/keywords`: Get keyword report.
    -   `GET /report/clustering`: Get clustering report.
    -   `GET, POST /feeds`: Manage RSS feeds.
    -   `DELETE /feeds/<int:feed_id>`: Delete a feed.

### Step 6: Application Factory (`app.py`)

-   Use the factory pattern (`create_app`) to construct the Flask application.
-   Initialize all extensions (SQLAlchemy, JWT, CORS, Mail).
-   Register the authentication and main blueprints.
-   Set up and start the `BackgroundScheduler` to run the `run_aggregation_for_all_users` job every 6 hours.

## 4. Testing Requirements

-   **`conftest.py`**: Create fixtures for the Flask `app`, `client`, and an `auth_token` for authenticated requests.
-   **`test_auth.py`**: Test user registration (success and duplicate) and login (success and failure).
-   **`test_documents.py`**: Test the full CRUD lifecycle of documents, including upload of supported and unsupported file types, listing, and deletion.
-   **`test_feeds.py`**: Test adding, listing, and deleting RSS feeds.
-   **`test_search.py`**: Mock the `RetrievalQA` chain and external APIs to test the search endpoint logic and the Bing fallback.
-   **`test_reports.py` and `test_clustering.py`**: Test the report generation endpoints, ensuring they handle cases with and without documents.
-   **`test_aggregation.py`**: Mock `feedparser` and `requests` to test that the aggregation service correctly processes RSS feeds and calls `add_document`.

Execute all instructions to produce a fully functional and tested backend that meets all documented requirements.
