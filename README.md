# XU-News-AI-RAG

XU-News-AI-RAG is a personalized, intelligent knowledge base system that automatically collects, organizes, and analyzes news content. It provides users with a powerful tool for information retrieval and insight discovery, leveraging a Retrieval-Augmented Generation (RAG) pipeline to answer questions based on a user-curated knowledge base.

## Features

- **Automated Data Collection:** Automatically gathers news from RSS feeds.
- **Personal Knowledge Base:** Users can upload their own documents (PDF, TXT, XLSX) to enrich their knowledge base.
- **Secure Authentication:** User registration and login functionality using JWT.
- **AI-Powered Search:** Ask questions in natural language to search the knowledge base.
- **Web Search Fallback:** If an answer is not found in the local knowledge base, the system can perform a web search to find the information.
- **Data Analysis:** Generate reports on keyword distribution and document clustering to identify trends.
- **Email Notifications:** System administrators can receive email notifications for new data ingestion.

## Technical Stack

- **Frontend:** React, Material-UI
- **Backend:** Flask, Python 3.11
- **Package Management:** `uv` (backend), `npm` (frontend)
- **Database:** SQLite (metadata), FAISS (vector storage)
- **AI Models:** Deployed via `llama-server`
  - **LLM:** `ggml-org/Qwen3-1.7B-GGUF`
  - **Embedding:** `ggml-org/embeddinggemma-300M-GGUF`
  - **Reranking:** `gpustack/bge-reranker-v2-m3-GGUF`

## Documentation

For a detailed understanding of the project's architecture, design, and requirements, please refer to the documents in the `/docs` directory:

- **[High-Level Design](docs/high-level-design.md)**
- **[Technical Architecture](docs/technical-architecture.md)**
- **[Product Prototype Design](docs/prototype-design.md)**
- **[Product Requirement Document (PRD)](docs/PRD.md)**

## Prerequisites

- [uv](https://github.com/astral-sh/uv)
- [Node.js and npm](https://nodejs.org/)
- A running `llama-server` instance from the [llama.cpp](https://github.com/ggml-org/llama.cpp) project. See `llama-server.md` for setup and model details.

## Setup and Installation

### 1. Backend

```bash
# Navigate to the backend directory
cd backend

# Install dependencies using uv
uv sync

# Create a .env file from the example
cp .env.example .env

# Update the .env file with your configuration
# (e.g., Llama server URLs, email settings)
```

### 2. Frontend

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies using npm
npm install
```

## Running the Application

### 1. Start the Llama Server

You must have a `llama-server` instance running with the required models loaded. Refer to the `llama-server.md` documentation for instructions on how to start the server.

### 2. Start the Backend Server

```bash
# From the backend directory
uv run gunicorn "backend.app:create_app()"
```
The backend server will start on `http://127.0.0.1:8000`.

### 3. Start the Frontend Application

```bash
# From the frontend directory
npm start
```
The frontend development server will start on `http://localhost:3000`.

## Running Tests

### Backend

```bash
# From the backend directory
uv run -m pytest
```

### Frontend

```bash
# From the frontend directory
npm test
```