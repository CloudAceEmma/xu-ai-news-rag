from unittest.mock import patch
from backend.services.custom_cross_encoder import LlamaServerCrossEncoder
from langchain_core.documents import Document

@patch('requests.post')
def test_llama_server_cross_encoder(mock_post):
    """Test the compress_documents method of the LlamaServerCrossEncoder."""
    mock_post.return_value.raise_for_status.return_value = None
    mock_post.return_value.json.return_value = {
        'results': [
            {'index': 1, 'relevance_score': 0.9},
            {'index': 0, 'relevance_score': 0.1}
        ]
    }

    encoder = LlamaServerCrossEncoder()
    docs = [
        Document(page_content="doc1"),
        Document(page_content="doc2")
    ]
    query = "test query"
    
    reranked_docs = encoder.compress_documents(docs, query)

    assert len(reranked_docs) == 2
    assert reranked_docs[0].page_content == "doc2" # index 1
    assert reranked_docs[1].page_content == "doc1" # index 0
    mock_post.assert_called_once()
