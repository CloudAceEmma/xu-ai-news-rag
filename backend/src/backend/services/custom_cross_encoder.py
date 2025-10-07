from langchain.retrievers.document_compressors.base import BaseDocumentCompressor
from langchain_core.documents import Document
from typing import List, Sequence
import requests
from backend.config import Config

class LlamaServerCrossEncoder(BaseDocumentCompressor):
    """Custom LangChain cross-encoder to rerank documents using a remote Llama server."""

    def compress_documents(
        self,
        documents: Sequence[Document],
        query: str,
        **kwargs: dict
    ) -> Sequence[Document]:
        """
        Rerank documents based on the query using the Llama reranking endpoint.
        """
        url = Config.RERANKING_URL
        if not url:
            raise ValueError("RERANKING_URL is not set in the configuration.")

        doc_contents = [doc.page_content for doc in documents]

        payload = {
            "model": "gpustack/bge-reranker-v2-m3-GGUF",
            "query": query,
            "documents": doc_contents
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            results = response.json().get('results', [])

            # Sort documents based on the 'relevance_score' from the reranking API
            # The API returns a list of dicts with 'index' and 'relevance_score'
            sorted_indices = [result['index'] for result in sorted(results, key=lambda x: x['relevance_score'], reverse=True)]

            # Create a new list of documents in the reranked order
            reranked_docs = [documents[i] for i in sorted_indices]
            return reranked_docs

        except requests.exceptions.RequestException as e:
            print(f"Error calling reranking service: {e}")
            # Fallback to returning original documents if reranking fails
            return list(documents)
