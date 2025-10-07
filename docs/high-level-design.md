# High-Level Design Document

## 1. Introduction

This document outlines the high-level design and architecture for the XU-News-AI-RAG system. The system is designed to be a personalized, intelligent knowledge base that automatically collects, organizes, and analyzes news content, providing users with a powerful tool for information retrieval and insight discovery.

## 2. System Architecture Overview

The system is composed of three main components:

1.  **Frontend:** A React-based single-page application (SPA) that provides the user interface for interacting with the system.
2.  **Backend:** A Flask-based server that exposes a RESTful API for the frontend to consume. It handles user authentication, data management, and orchestrates the AI-powered search and analysis.
3.  **AI Services:** A `llama-server` instance that provides the core AI capabilities, including language modeling, text embedding, and reranking.

```
+-----------------+      +-----------------+      +----------------+
|                 |      |                 |      |                |
|    Frontend     |----->|     Backend     |----->|   llama-server |
| (React UI)      |      |  (Flask API)    |      | (AI Services)  |
|                 |      |                 |      |                |
+-----------------+      +-------+---------+      +----------------+
                                 |
                                 |
                       +---------v---------+
                       |                   |
                       |  SQLite & FAISS   |
                       |    (Database)     |
                       |                   |
                       +-------------------+
```

## 3. Core Components and Functionality

### 3.1. Frontend

-   **User Interface:** A clean, modern UI built with React and Material-UI.
-   **Authentication:** A login/register page for user authentication.
-   **Dashboard:** A central dashboard for managing documents, RSS feeds, running searches, and viewing reports.
-   **State Management:** Local component state and JWT tokens for session management.

### 3.2. Backend

-   **API Server:** A Flask application serving a RESTful API.
-   **User Management:** Handles user registration, login, and session management via JWT.
-   **Knowledge Base Management:** Provides CRUD operations for documents and RSS feeds.
-   **RAG Pipeline Orchestration:** Manages the process of receiving a query, retrieving relevant documents, reranking them, and generating an answer using the LLM.
-   **Background Tasks:** An `apscheduler` instance to periodically fetch and process RSS feeds.

### 3.3. AI Services (`llama-server`)

-   **LLM Endpoint:** Provides access to a Large Language Model for text generation and summarization.
-   **Embedding Endpoint:** Generates vector embeddings for text documents.
-   **Reranking Endpoint:** Reranks search results for improved relevance.

## 4. User Flows

### 4.1. User Registration and Login

1.  User navigates to the web application.
2.  User registers for a new account or logs in with existing credentials.
3.  The backend authenticates the user and returns a JWT.
4.  The frontend stores the JWT and provides access to the dashboard.

### 4.2. Document Upload and Management

1.  User uploads a document (PDF, TXT, XLSX) via the dashboard.
2.  The backend receives the file, chunks it, generates embeddings, and stores them in the user's FAISS index.
3.  Metadata is stored in the SQLite database.
4.  User can view, edit metadata for, and delete documents from the dashboard.

### 4.3. Search and Information Retrieval (RAG)

1.  User submits a natural language query through the search bar.
2.  The backend receives the query and generates an embedding for it.
3.  The backend searches the user's FAISS index for relevant document chunks.
4.  The retrieved chunks are reranked for relevance.
5.  The query and the top-ranked chunks are passed to the LLM to generate an answer.
6.  The answer is returned to the frontend and displayed to the user.

## 5. Data Management

-   **Metadata:** Stored in a SQLite database, managed by SQLAlchemy. This includes user information, document metadata, and RSS feed URLs.
-   **Vector Data:** Stored in user-specific FAISS indexes on the file system. Each user has their own index to ensure data isolation.
-   **Uploaded Files:** Original uploaded files are stored on the backend's file system.
