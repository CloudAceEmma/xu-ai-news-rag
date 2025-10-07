from unittest.mock import patch

@patch('backend.routes.main.perform_search')
def test_search_endpoint(mock_perform_search, client, auth_token):
    """Test the search endpoint, mocking the search service."""
    mock_perform_search.return_value = {"answer": "This is a test answer.", "source": "Local Knowledge Base"}
    
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = client.post('/api/search', json={'query': 'test query'}, headers=headers)
    
    assert response.status_code == 200
    assert response.get_json()['answer'] == "This is a test answer."
    mock_perform_search.assert_called_once()

@patch('backend.services.search._bing_search')
@patch('os.path.exists', return_value=False)
def test_search_fallback_to_bing(mock_exists, mock_bing_search, client, auth_token):
    """Test that the search logic falls back to Bing when no local index exists."""
    mock_bing_search.return_value = "Answer from Bing."
    
    from backend.services.search import perform_search
    user_id = 1 # In a real test, you might get this from the token
    result = perform_search(user_id, "query with no local results")
    
    assert result['source'] == "Web Search"
    assert result['answer'] == "Answer from Bing."
    mock_exists.assert_called()
    mock_bing_search.assert_called_once()
