# Product Prototype Design

## 1. Introduction

This document describes the design and user flow of the XU-News-AI-RAG web application prototype. Since a visual design file is not available, this document serves as a textual and structural representation of the user interface.

## 2. Overall Design Philosophy

The UI is designed to be clean, modern, and intuitive, following the principles of Material Design. The layout is responsive and works well on modern web browsers.

## 3. Page and Component Breakdown

### 3.1. Authentication Page (`/auth`)

-   **Layout:** A centered form on a clean background.
-   **Components:**
    -   A toggle to switch between "Sign In" and "Sign Up" forms.
    -   **Login Form:**
        -   Username field
        -   Password field
        -   "Sign In" button
    -   **Register Form:**
        -   Username field
        -   Password field
        -   "Sign Up" button
-   **User Flow:**
    1.  A new user can register for an account.
    2.  An existing user can log in.
    3.  Upon successful login, the user is redirected to the `/dashboard` page.

### 3.2. Dashboard Page (`/dashboard`)

This is the main page for authenticated users. It is laid out as a grid of components.

-   **Layout:** A responsive grid that organizes the various dashboard widgets.
-   **Components:**
    -   **Header:** A persistent header with the application title and a "Logout" button.
    -   **Search Bar:** A prominent search bar at the top of the page for asking natural language questions.
        -   Displays the answer and the source of the information (Local Knowledge Base or Web Search) below the search bar after a search is performed.
    -   **Upload Form:** A card for uploading new documents.
        -   Includes a file input, and text fields for "Source" and "Tags".
    -   **Feed Manager:** A card for managing RSS feeds.
        -   Includes a text field to add a new feed URL and a list of existing feeds with delete buttons.
    -   **Document List:** A list of all documents in the user's knowledge base.
        -   Each item shows the document's name, type, source, and tags.
        -   Includes "Edit" and "Delete" buttons for each document.
        -   An editing form appears when "Edit" is clicked.
    -   **Reports:** A card for generating and viewing reports.
        -   Buttons to "Generate Keywords Report" and "Generate Clustering Report".
        -   Displays the reports (top keywords, document clusters) when generated.

## 4. User Interaction Flow

1.  **Login:** User logs in and is taken to the dashboard.
2.  **Add Data:**
    -   User adds a few RSS feeds to start automatic data collection.
    -   User uploads a personal PDF document.
3.  **Search:**
    -   User asks a question related to the uploaded document.
    -   The system finds the answer in the document and displays it.
4.  **Analyze:**
    -   User generates the "Keywords Report" to see the main themes in their knowledge base.
5.  **Manage:**
    -   User edits the tags of the uploaded document to better categorize it.
    -   User deletes an old, irrelevant document.
