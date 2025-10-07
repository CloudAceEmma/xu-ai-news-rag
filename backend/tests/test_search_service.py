from unittest.mock import patch
from backend.services.embedding import LlamaServerEmbeddings

@patch('requests.post')
def test_llama_server_embed_documents(mock_post):
    """Test the embed_documents method of the LlamaServerEmbeddings."""
    mock_post.return_value.raise_for_status.return_value = None
    mock_post.return_value.json.return_value = {
        'data': [
            {'embedding': [0.1, 0.2]},
            {'embedding': [0.3, 0.4]}
        ]
    }

    embeddings = LlamaServerEmbeddings()
    texts = ["text1", "text2"]
    result = embeddings.embed_documents(texts)

    assert result == [[0.1, 0.2], [0.3, 0.4]]
    mock_post.assert_called_once()

@patch('requests.post')
def test_llama_server_embed_query(mock_post):
    """Test the embed_query method of the LlamaServerEmbeddings."""
    mock_post.return_value.raise_for_status.return_value = None
    mock_post.return_value.json.return_value = {
        'data': [{'embedding': [0.5, 0.6]}]
    }

    embeddings = LlamaServerEmbeddings()
    text = "query text"
    result = embeddings.embed_query(text)

    assert result == [0.5, 0.6]
    mock_post.assert_called_once()
