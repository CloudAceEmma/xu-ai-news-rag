from unittest.mock import patch

@patch('backend.routes.main.generate_keyword_report')
def test_keyword_report_endpoint(mock_generate_report, client, auth_token):
    """Test the keyword report endpoint."""
    mock_generate_report.return_value = {"top_keywords": ["test", "keyword"]}
    
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = client.get('/api/report/keywords', headers=headers)
    
    assert response.status_code == 200
    assert response.get_json()['top_keywords'] == ["test", "keyword"]
    mock_generate_report.assert_called_once()

def test_keyword_report_no_documents(client, auth_token):
    """Test keyword report generation with no documents."""
    from backend.services.search import generate_keyword_report
    # Assuming the test user is created via auth_token fixture and has id=1
    report = generate_keyword_report(user_id=1)
    assert "error" in report
