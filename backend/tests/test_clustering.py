from unittest.mock import patch

@patch('backend.routes.main.generate_cluster_report')
def test_clustering_report_endpoint(mock_generate_report, client, auth_token):
    """Test the clustering report endpoint."""
    mock_generate_report.return_value = {"Cluster 1": ["test", "cluster"]}
    
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = client.get('/api/report/clustering', headers=headers)
    
    assert response.status_code == 200
    assert response.get_json()['Cluster 1'] == ["test", "cluster"]
    mock_generate_report.assert_called_once()

def test_clustering_report_no_documents(client, auth_token):
    """Test cluster report generation with no documents."""
    from backend.services.clustering import generate_cluster_report
    # Assuming the test user is created via auth_token fixture and has id=1
    report = generate_cluster_report(user_id=1)
    assert "error" in report
