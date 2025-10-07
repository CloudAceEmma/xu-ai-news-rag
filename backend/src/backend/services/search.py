from backend.services.embedding import LlamaServerEmbeddings
from typing import List
import requests
from backend.config import Config
from langchain_community.vectorstores import FAISS
from langchain.retrievers import ContextualCompressionRetriever
from langchain.chains import RetrievalQA
from backend.services.custom_llm import LlamaServerLLM
from backend.services.custom_cross_encoder import LlamaServerCrossEncoder
from backend.models import Document
from sklearn.feature_extraction.text import CountVectorizer
import os



def _bing_search(query: str) -> str:
    """Performs a web search using the Bing Search API and returns a summary."""
    if not Config.BING_API_KEY or not Config.BING_SEARCH_URL:
        return "Web search is not configured."

    headers = {"Ocp-Apim-Subscription-Key": Config.BING_API_KEY}
    params = {"q": query, "count": 3}
    
    try:
        response = requests.get(Config.BING_SEARCH_URL, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        
        snippets = [result['snippet'] for result in search_results.get('webPages', {}).get('value', [])]
        if not snippets:
            return "No relevant information found on the web."
            
        # Use the LLM to summarize the snippets
        summary_prompt = f"Summarize the following search results for the query '{query}':\n\n" + "\n".join(snippets)
        llm = LlamaServerLLM()
        summary = llm._call(summary_prompt)
        return summary
    except requests.RequestException as e:
        return f"Error during web search: {e}"

def perform_search(user_id, query):
    """
    Performs a search in the user's knowledge base using a RAG pipeline.
    Falls back to web search if no local results are found.
    """
    index_path = os.path.join(Config.FAISS_INDEX_PATH, f"user_{user_id}")

    if not os.path.exists(index_path):
        return {"answer": _bing_search(query), "source": "Web Search", "source_documents": []}

    embeddings = LlamaServerEmbeddings()
    
    try:
        vector_store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    except Exception as e:
        print(f"Error loading FAISS index: {e}")
        return {"answer": _bing_search(query), "source": "Web Search", "source_documents": []}

    # 1. Create a base retriever
    base_retriever = vector_store.as_retriever(search_kwargs={"k": 10})

    # 2. Create a reranker
    reranker = LlamaServerCrossEncoder()
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=reranker, base_retriever=base_retriever
    )
    
    # 3. Create the RetrievalQA chain
    llm = LlamaServerLLM()
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=compression_retriever,
        return_source_documents=True,
    )
    
    result = qa_chain({"query": query})

    if not result.get("source_documents"):
        # Fallback to web search if no relevant documents are found
        return {"answer": _bing_search(query), "source": "Web Search", "source_documents": []}

    return {
        "answer": result["result"],
        "source": "Local Knowledge Base",
        "source_documents": [
            {
                "page_content": doc.page_content,
                "metadata": doc.metadata
            } for doc in result["source_documents"]
        ]
    }


def generate_keyword_report(user_id):
    """
    Generates a report of the top 10 keywords from a user's documents.
    """
    docs = Document.query.filter_by(user_id=user_id).all()
    if not docs:
        return {"error": "No documents found for this user."}

    doc_contents = []
    for doc in docs:
        try:
            with open(doc.file_path, 'r', encoding='utf-8') as f:
                doc_contents.append(f.read())
        except Exception as e:
            print(f"Could not read file {doc.file_path}: {e}")
            continue
    
    if not doc_contents:
        return {"error": "Could not read any documents."}

    vectorizer = CountVectorizer(stop_words='english', max_features=10)
    vectorizer.fit_transform(doc_contents)
    
    return {"top_keywords": vectorizer.get_feature_names_out().tolist()}
