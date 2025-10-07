from unittest.mock import patch, MagicMock
from backend.services.search import perform_search, _bing_search
from backend.config import Config

@patch('backend.services.search._bing_search')
@patch('os.path.exists', return_value=False)
def test_perform_search_no_index_fallback_to_bing(mock_exists, mock_bing):
    """Test that perform_search falls back to Bing search when no FAISS index exists."""
    mock_bing.return_value = "Bing result"
    result = perform_search(user_id=1, query="test query")
    assert result == {'answer': 'Bing result', 'source': 'Web Search', 'source_documents': []}
    mock_bing.assert_called_once_with("test query")

@patch('langchain.chains.RetrievalQA.from_chain_type')
@patch('backend.services.search.FAISS.load_local')
@patch('os.path.exists', return_value=True)
def test_perform_search_with_local_kb(mock_exists, mock_load_local, mock_from_chain_type):
    """Test that perform_search uses the local RAG pipeline."""
    from langchain_core.runnables import Runnable
    # Mock the vector store and retriever
    mock_retriever = MagicMock(spec=Runnable)
    mock_vector_store = MagicMock()
    mock_vector_store.as_retriever.return_value = mock_retriever
    mock_load_local.return_value = mock_vector_store

    # Mock the QA chain
    mock_qa_chain = MagicMock()
    mock_qa_chain.return_value = {
        "result": "Local KB answer",
        "source_documents": [MagicMock(page_content="doc1", metadata={})]
    }
    mock_from_chain_type.return_value = mock_qa_chain

    result = perform_search(user_id=1, query="test query")

    assert result['answer'] == "Local KB answer"
    assert result['source'] == "Local Knowledge Base"
    assert len(result['source_documents']) == 1
    mock_qa_chain.assert_called_once_with({"query": "test query"})


def test_bing_search_not_configured():
    """Test _bing_search when API key or URL is not configured."""
    with patch.object(Config, 'BING_API_KEY', None):
        result = _bing_search("test query")
        assert result == "Web search is not configured."

@patch('requests.get')
def test_bing_search_request_exception(mock_get):
    """Test _bing_search when the web request fails."""
    import requests
    mock_get.side_effect = requests.exceptions.RequestException("Test error")
    result = _bing_search("test query")
    assert "Error during web search" in result

@patch('backend.services.search.LlamaServerLLM')
@patch('requests.get')
def test_bing_search_success(mock_get, mock_llm):
    """Test _bing_search successful path."""
    mock_get.return_value.raise_for_status.return_value = None
    mock_get.return_value.json.return_value = {
        'webPages': {
            'value': [{'snippet': 'Test snippet'}]
        }
    }
    mock_llm.return_value._call.return_value = "Summarized result"

    result = _bing_search("test query")
    assert result == "Summarized result"
    mock_llm.return_value._call.assert_called_once()
