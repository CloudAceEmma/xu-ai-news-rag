def test_add_feed_success(client, auth_token):
    """Test successfully adding a new RSS feed."""
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = client.post('/api/feeds', json={'url': 'http://test.com/rss'}, headers=headers)
    
    assert response.status_code == 201
    assert 'id' in response.get_json()
    assert response.get_json()['url'] == 'http://test.com/rss'

def test_add_feed_missing_url(client, auth_token):
    """Test adding a feed with no URL provided."""
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = client.post('/api/feeds', json={}, headers=headers)
    
    assert response.status_code == 400
    assert response.get_json()['error'] == "URL is required"

def test_get_feeds(client, auth_token):
    """Test retrieving all feeds for a user."""
    headers = {'Authorization': f'Bearer {auth_token}'}
    # Add a feed first
    client.post('/api/feeds', json={'url': 'http://test.com/rss'}, headers=headers)
    
    # Retrieve the list of feeds
    response = client.get('/api/feeds', headers=headers)
    
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
    assert len(response.get_json()) == 1
    assert response.get_json()[0]['url'] == 'http://test.com/rss'

def test_delete_feed(client, auth_token):
    """Test deleting a feed."""
    headers = {'Authorization': f'Bearer {auth_token}'}
    # Add a feed to get its ID
    add_response = client.post('/api/feeds', json={'url': 'http://todelete.com/rss'}, headers=headers)
    feed_id = add_response.get_json()['id']
    
    # Delete the feed
    delete_response = client.delete(f'/api/feeds/{feed_id}', headers=headers)
    
    assert delete_response.status_code == 200
    assert delete_response.get_json()['message'] == "Feed deleted"
    
    # Verify the feed is gone
    get_response = client.get('/api/feeds', headers=headers)
    assert len(get_response.get_json()) == 0
