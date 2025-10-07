from langchain_core.embeddings import Embeddings
from typing import List
import requests
from backend.config import Config

class LlamaServerEmbeddings(Embeddings):
    """
    Custom LangChain Embeddings class to interact with a remote Llama server
    for generating text embeddings.
    """

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of documents.
        """
        url = Config.EMBEDDING_URL
        if not url:
            raise ValueError("EMBEDDING_URL is not set in the configuration.")

        try:
            response = requests.post(
                url,
                json={
                    "input": texts,
                    "model": "ggml-org/embeddinggemma-300M-GGUF"
                }
            )
            response.raise_for_status()
            embeddings = [item['embedding'] for item in response.json()['data']]
            return embeddings
        except requests.exceptions.RequestException as e:
            print(f"Error calling embedding service: {e}")
            return [[] for _ in texts]

    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query.
        """
        url = Config.EMBEDDING_URL
        if not url:
            raise ValueError("EMBEDDING_URL is not set in the configuration.")

        try:
            response = requests.post(
                url,
                json={
                    "input": text,
                    "model": "ggml-org/embeddinggemma-300M-GGUF"
                }
            )
            response.raise_for_status()
            return response.json()['data'][0]['embedding']
        except requests.exceptions.RequestException as e:
            print(f"Error calling embedding service: {e}")
            return []
