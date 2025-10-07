# Product Requirement Document (PRD) for XU-News-AI-RAG

---

## 1. Introduction

### 1.1. Background
In the current information age, users are inundated with vast amounts of news and data from various sources. It is challenging to efficiently aggregate, manage, and retrieve relevant information. The XU-News-AI-RAG project aims to solve this problem by creating a personalized, intelligent knowledge base that automatically collects, organizes, and analyzes news content, providing users with a powerful tool for information retrieval and insight discovery.

### 1.2. Target Users
*   **Information Professionals & Researchers:** Individuals who need to track specific topics or industries and require a centralized, searchable repository of news and articles.
*   **Content Creators & Journalists:** Professionals who need to quickly find source materials, verify facts, and identify trends from a reliable information base.
*   **Lifelong Learners:** Individuals with a curiosity for specific subjects who want a personalized news feed and a way to explore topics in depth.

### 1.3. Product Vision
To build an intelligent, automated, and personalized news knowledge base system that empowers users to effortlessly stay informed and derive meaningful insights from the world's information.

---

## 2. User Stories and Scenario Descriptions

### 2.1. Data Collection
*   **As a user, I want to** automatically gather news from various sources like RSS feeds and websites, **so that** I can save time and have all my information in one place.
*   **As a system administrator, I want to** receive an email notification when new data is successfully added to the knowledge base, **so that** I can monitor the system's activity.

### 2.2. User and Authentication
*   **As a user, I want to** create an account and log in securely, **so that** I can access my personalized knowledge base.

### 2.3. Knowledge Management
*   **As a user, I want to** view a list of all the data in my knowledge base, **so that** I can get an overview of my collected information.
*   **As a user, I want to** filter the data list by type (e.g., article, document) and time, **so that** I can find specific information quickly.
*   **As a user, I want to** edit the metadata of my data, such as tags and sources, **so that** I can better organize my knowledge base.
*   **As a user, I want to** delete single or multiple items from my knowledge base, **so that** I can remove irrelevant or outdated information.
*   **As a user, I want to** upload my own files (e.g., PDFs, Excel sheets) through a web interface, **so that** I can enrich my knowledge base with personal documents.

### 2.4. Information Retrieval
*   **As a user, I want to** ask questions in natural language, **so that** I can easily find the most relevant information within my knowledge base.
*   **As a user, when** my knowledge base doesn't contain the answer to my query, **I want the system to** automatically search the web and provide a summarized answer, **so that** I can still get the information I need.

### 2.5. Data Analysis
*   **As a user, I want to** see a report of the Top 10 keyword distributions, **so that** I can understand the main themes and trends within my knowledge base.

---

## 3. Product Scope and Feature List

### 3.1. Data Ingestion
*   **Scheduled Tasks:** Automated mechanism for fetching news via RSS, web scraping, and intelligent agents.
*   **Data Import:** Support for writing both structured (Excel) and unstructured data to the knowledge base via an API.
*   **Manual Upload:** Web interface for users to upload various data types.

### 3.2. User & Notifications
*   **User Authentication:** Secure user login functionality using JWT.
*   **Email Notifications:** Automated emails upon successful data ingestion, with customizable title and content.

### 3.3. Knowledge Base Management
*   **Data Viewing:** A filterable list view of all knowledge base content (filterable by type/time).
*   **Data Editing:** Ability to modify metadata such as tags and sources.
*   **Data Deletion:** Single and batch deletion of knowledge base entries.

### 3.4. AI-Powered Search & Analysis
*   **Semantic Query:** Natural language-based search of the knowledge base, with results ranked by similarity.
*   **Web Search Fallback:** If no relevant data is found in the knowledge base, the system will perform an online search (e.g., Bing API) and return the top 3 summarized results.
*   **Clustering Analysis:** Generation of a report displaying the Top 10 keyword distribution in the knowledge base.

---

## 4. Product-Specific AI Requirements

### 4.1. Model Requirements
*   **Large Language Model (LLM):**
    *   **Function:** Used for inference, summarization of web search results, and powering semantic query understanding.
    *   **Model:** Deployed via llama-server, `qwen2.5::3b` is recommended.
*   **Embedding Model:**
    *   **Function:** To convert text data into vector representations for storage and similarity search.
    *   **Model:** `all-MiniLM-L6-v2` is recommended.
*   **Reranking Model:**
    *   **Function:** To improve the relevance of search results retrieved from the knowledge base.
    *   **Model:** `ms-marco-MiniLM-L-6-v2` is recommended.

### 4.2. Data Requirements
*   **Source:** RSS feeds, web-scraped articles, and user-uploaded documents.
*   **Quantity:** The system must be designed to handle a continuously growing dataset.
*   **Quality:** Data ingestion pipelines should include steps for basic cleaning and formatting.
*   **Annotation:** Metadata (ID, type, source, tags, timestamp) will be stored in a relational database (SQLite). Vector data will be stored in a vector database (FAISS).

### 4.3. Algorithm Boundaries and Interpretability
*   The system's primary knowledge source is the user-curated knowledge base.
*   For queries outside the knowledge base, the system is limited to the information present in the top 3 web search results.
*   The system should, where possible, cite the source of the information provided in its answers.

### 4.4. Evaluation Criteria
*   **Search Relevance:** Measured by the precision and recall of the semantic search results.
*   **Response Quality:** The accuracy, coherence, and conciseness of the LLM-generated summaries.
*   **Keyword Analysis:** The accuracy and relevance of the Top 10 keywords identified in the clustering report.

### 4.5. Ethics and Compliance
*   **Web Scraping:** All web scraping activities must comply with website `robots.txt` files and terms of service to ensure ethical data collection.
*   **Data Privacy:** User data and the contents of their knowledge base must be kept secure and private.

---

## 5. Technical Stack

*   **AI Framework:** The core business logic will be developed and orchestrated using the **LangChain** framework to support the construction and retrieval-augmented generation (RAG) for the knowledge base.
*   **Frontend:** React
*   **Backend:** golang gin
*   **Relational Database:** SQLite (for metadata)
*   **Vector Database:** FAISS (for vector data)

---

## 6. Non-Functional Requirements

*   **Performance:**
    *   Semantic search queries should return results in under 3 seconds.
    *   The data ingestion process should be efficient and not block user-facing operations.
*   **Security:**
    *   User authentication will be implemented using JWT.
    *   The application must be protected against common web vulnerabilities (e.g., XSS, SQL injection).
*   **Usability:**
    *   The web interface should be intuitive, responsive, and easy to navigate.
*   **Scalability:**
    *   The architecture should allow for the growth of the user base and the volume of data in the knowledge base.
*   **Reliability:**
    *   The system should have a high uptime and be resilient to errors in the data ingestion pipeline.

---

## 7. Release Criteria and Measurement Indicators

### 7.1. Release Criteria
*   All features listed in Section 3 are implemented and have passed unit, integration, and API tests.
*   The application is successfully deployed and operational.
*   There are no critical or blocking bugs.
*   All required documentation (HLD, Technical Architecture, README.md) is complete.

### 7.2. Measurement Indicators
*   **User Engagement:** Daily/Monthly active users.
*   **System Usage:** Number of queries per day, number of documents added per week.
*   **Performance:** Average query response time, system uptime percentage.
*   **User Satisfaction:** Feedback surveys and ratings.

---

## 8. Pending Items and Future Plans

### 8.1. Pending Items
*   Finalize the specific UI/UX design for the web interface.
*   Define the exact schema for structured data import via Excel.
*   Select and configure the initial set of RSS feeds for data collection.

### 8.2. Future Plans
*   **Enhanced Analytics:** Introduce more advanced data visualization and trend analysis features.
*   **Multi-User Collaboration:** Add features for teams to share and collaborate on knowledge bases.
*   **Expanded Data Sources:** Integrate with more third-party services and APIs (e.g., Twitter, news APIs).
*   **Mobile Application:** Develop a mobile client for on-the-go access to the knowledge base.
