# Technical Architecture Document

## 1. Introduction

This document provides a detailed technical overview of the XU-News-AI-RAG system, covering the backend, frontend, and AI service integrations.

## 2. Backend Architecture

The backend is a monolithic Flask application written in Python 3.11. It follows a standard service-oriented architecture.

-   **Framework:** Flask
-   **Package Manager:** `uv`
-   **WSGI Server:** Gunicorn
-   **Database ORM:** SQLAlchemy
-   **Authentication:** JWT

### 2.1. Project Structure

```
src/backend/
├── app.py          # Application factory
├── config.py       # Configuration management
├── models.py       # SQLAlchemy models
├── auth/
│   └── routes.py   # Authentication endpoints
├── routes/
│   └── main.py     # Main API endpoints
└── services/
    ├── aggregation.py  # RSS feed aggregation
    ├── clustering.py   # Document clustering
    ├── knowledge_base.py # Document processing and FAISS interaction
    ├── search.py       # RAG pipeline and search logic
    └── ...             # Other services
```

### 2.2. Database Schema

-   **`User`**
    -   `id` (Integer, Primary Key)
    -   `username` (String, Unique)
    -   `password_hash` (String)
-   **`Document`**
    -   `id` (Integer, Primary Key)
    -   `user_id` (Integer, Foreign Key to `User.id`)
    -   `file_path` (String)
    -   `document_type` (String)
    -   `source` (String)
    -   `tags` (String)
    -   `uploaded_at` (DateTime)
-   **`RssFeed`**
    -   `id` (Integer, Primary Key)
    -   `user_id` (Integer, Foreign Key to `User.id`)
    -   `url` (String)

### 2.3. API Endpoints

See the `routes/main.py` and `auth/routes.py` files for the full API specification. All endpoints under `/api/` (except for auth) are protected by JWT.

### 2.4. RAG Pipeline Implementation

1.  **Query Embedding:** The user's query is embedded using the `LlamaServerEmbeddings` class, which calls the `llama-server`'s `/v1/embeddings` endpoint.
2.  **Vector Search:** The user's FAISS index is searched for the `k` most similar document chunks.
3.  **Reranking:** The retrieved chunks are reranked using the `LlamaServerCrossEncoder`, which calls the `/rerank` endpoint.
4.  **Answer Generation:** The query and the reranked chunks are passed to the `LlamaServerLLM`, which calls the `/v1/chat/completions` endpoint to generate the final answer.

## 3. Frontend Architecture

The frontend is a single-page application built with React.

-   **Framework:** React
-   **Package Manager:** npm
-   **UI Library:** Material-UI
-   **API Client:** Axios

### 3.1. Project Structure

```
src/
├── App.js              # Main application component and routing
├── api/
│   └── axiosConfig.js  # Axios client configuration
├── components/
│   ├── Auth/           # Login and Register components
│   ├── Common/         # Shared components (Header, PrivateRoute)
│   └── Dashboard/      # Dashboard components
└── pages/
    ├── AuthPage.js     # Page for authentication
    └── DashboardPage.js # Main dashboard page
```

### 3.2. State and Session Management

-   The JWT received from the backend is stored in `localStorage`.
-   An Axios interceptor injects the JWT into the `Authorization` header of all outgoing requests.
-   The application state is managed within React components.

## 4. AI Services Integration

The system relies on a `llama-server` instance for its AI capabilities. The backend communicates with this server via HTTP requests. The URLs for the `llama-server` endpoints are configured via environment variables.

-   **LLM:** `POST /v1/chat/completions`
-   **Embedding:** `POST /v1/embeddings`
-   **Reranking:** `POST /rerank`

It is crucial that the `llama-server` is started with the correct models loaded to serve these endpoints.
