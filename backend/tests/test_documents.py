import os
from io import BytesIO
from unittest.mock import patch

@patch('os.path.exists', return_value=False)
@patch('backend.services.knowledge_base.FAISS.from_documents')
@patch('backend.services.knowledge_base.FAISS.load_local')
@patch('backend.services.knowledge_base.LlamaServerEmbeddings')
def test_upload_document_success(mock_embeddings, mock_load, mock_faiss, mock_exists, client, auth_token):
    """Test successful document upload."""
    mock_embeddings.return_value.embed_documents.return_value = [[0.1] * 768]
    data = {
        'file': (BytesIO(b'this is a test txt file'), 'test.txt'),
        'source': 'local',
        'tags': 'testing'
    }
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = client.post('/api/documents', data=data, headers=headers, content_type='multipart/form-data')
    
    assert response.status_code == 201
    assert response.get_json()['msg'] == "File uploaded and processed successfully"

def test_upload_unsupported_file_type(client, auth_token):
    """Test uploading a file with an unsupported extension."""
    data = {
        'file': (BytesIO(b'this is a test file'), 'test.unsupported'),
    }
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = client.post('/api/documents', data=data, headers=headers, content_type='multipart/form-data')
    
    assert response.status_code == 400
    assert response.get_json()['msg'] == "File type not allowed"

@patch('os.path.exists', return_value=False)
@patch('backend.services.knowledge_base.FAISS.from_documents')
@patch('backend.services.knowledge_base.FAISS.load_local')
@patch('backend.services.knowledge_base.LlamaServerEmbeddings')
def test_get_documents(mock_embeddings, mock_load, mock_faiss, mock_exists, client, auth_token):
    """Test retrieving a list of documents for a user."""
    mock_embeddings.return_value.embed_documents.return_value = [[0.1] * 768]
    # First, upload a document
    client.post('/api/documents', data={
        'file': (BytesIO(b'content'), 'test.txt')
    }, headers={'Authorization': f'Bearer {auth_token}'}, content_type='multipart/form-data')

    # Then, get the list
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = client.get('/api/documents', headers=headers)
    
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
    assert len(response.get_json()) > 0
    assert response.get_json()[0]['document_type'] == 'txt'

@patch('os.path.exists', return_value=False)
@patch('backend.services.knowledge_base.FAISS.from_documents')
@patch('backend.services.knowledge_base.FAISS.load_local')
@patch('backend.services.knowledge_base.LlamaServerEmbeddings')
def test_delete_document(mock_embeddings, mock_load, mock_faiss, mock_exists, client, auth_token):
    """Test deleting a document."""
    mock_embeddings.return_value.embed_documents.return_value = [[0.1] * 768]
    # Upload a document to get an ID
    upload_resp = client.post('/api/documents', data={
        'file': (BytesIO(b'content'), 'delete_me.txt')
    }, headers={'Authorization': f'Bearer {auth_token}'}, content_type='multipart/form-data')
    
    # Get the document ID from the listing
    list_resp = client.get('/api/documents', headers={'Authorization': f'Bearer {auth_token}'})
    doc_id = list_resp.get_json()[0]['id']

    # Delete the document
    delete_resp = client.delete(f'/api/documents/{doc_id}', headers={'Authorization': f'Bearer {auth_token}'})
    
    assert delete_resp.status_code == 200
    assert delete_resp.get_json()['msg'] == "Document deleted"

    # Verify it's gone
    list_after_delete = client.get('/api/documents', headers={'Authorization': f'Bearer {auth_token}'})
    assert len(list_after_delete.get_json()) == 0

@patch('os.path.exists', return_value=False)
@patch('backend.services.knowledge_base.FAISS.from_documents')
@patch('backend.services.knowledge_base.FAISS.load_local')
@patch('backend.services.knowledge_base.LlamaServerEmbeddings')
def test_update_document(mock_embeddings, mock_load, mock_faiss, mock_exists, client, auth_token):
    """Test updating a document's metadata."""
    mock_embeddings.return_value.embed_documents.return_value = [[0.1] * 768]
    headers = {'Authorization': f'Bearer {auth_token}'}
    
    # Upload a document
    client.post('/api/documents', data={
        'file': (BytesIO(b'content'), 'updatable.txt'),
        'source': 'initial_source',
        'tags': 'initial_tags'
    }, headers=headers, content_type='multipart/form-data')

    # Get the document ID
    list_resp = client.get('/api/documents', headers=headers)
    doc_id = list_resp.get_json()[0]['id']

    # Update the document
    update_data = {'source': 'updated_source', 'tags': 'updated_tags'}
    update_resp = client.put(f'/api/documents/{doc_id}', json=update_data, headers=headers)
    
    assert update_resp.status_code == 200
    assert update_resp.get_json()['msg'] == "Document updated"

    # Verify the update
    list_after_update = client.get('/api/documents', headers=headers)
    updated_doc = list_after_update.get_json()[0]
    assert updated_doc['source'] == 'updated_source'
    assert updated_doc['tags'] == 'updated_tags'

@patch('os.path.exists', return_value=False)
@patch('backend.services.knowledge_base.FAISS.from_documents')
@patch('backend.services.knowledge_base.FAISS.load_local')
@patch('backend.services.knowledge_base.LlamaServerEmbeddings')
def test_get_documents_with_filters(mock_embeddings, mock_load, mock_faiss, mock_exists, client, auth_token):
    """Test filtering documents by type and date."""
    mock_embeddings.return_value.embed_documents.return_value = [[0.1] * 768]
    headers = {'Authorization': f'Bearer {auth_token}'}

    # Upload a few documents
    client.post('/api/documents', data={'file': (BytesIO(b'txt content'), 'test.txt')}, headers=headers, content_type='multipart/form-data')
    with open('tests/testdata/test.pdf', 'rb') as f:
        client.post('/api/documents', data={'file': (f, 'test.pdf')}, headers=headers, content_type='multipart/form-data')

    # Test filtering by type
    response_txt = client.get('/api/documents?type=txt', headers=headers)
    assert response_txt.status_code == 200
    assert len(response_txt.get_json()) == 1
    assert response_txt.get_json()[0]['document_type'] == 'txt'

    response_pdf = client.get('/api/documents?type=pdf', headers=headers)
    assert response_pdf.status_code == 200
    assert len(response_pdf.get_json()) == 1
    assert response_pdf.get_json()[0]['document_type'] == 'pdf'
    
    # Test filtering by date (assuming uploads are within the same day)
    from datetime import date, timedelta
    today = date.today().isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    response_date = client.get(f'/api/documents?start_date={today}&end_date={tomorrow}', headers=headers)
    assert response_date.status_code == 200
    assert len(response_date.get_json()) == 2

@patch('os.path.exists', return_value=False)
@patch('backend.services.knowledge_base.FAISS.from_documents')
@patch('backend.services.knowledge_base.FAISS.load_local')
@patch('backend.services.knowledge_base.LlamaServerEmbeddings')
def test_batch_delete_documents(mock_embeddings, mock_load, mock_faiss, mock_exists, client, auth_token):
    """Test deleting multiple documents in a batch."""
    mock_embeddings.return_value.embed_documents.return_value = [[0.1] * 768]
    headers = {'Authorization': f'Bearer {auth_token}'}

    # Upload documents
    client.post('/api/documents', data={'file': (BytesIO(b''), 'doc1.txt')}, headers=headers, content_type='multipart/form-data')
    client.post('/api/documents', data={'file': (BytesIO(b''), 'doc2.txt')}, headers=headers, content_type='multipart/form-data')
    
    # Get their IDs
    list_resp = client.get('/api/documents', headers=headers)
    doc_ids = [doc['id'] for doc in list_resp.get_json()]
    assert len(doc_ids) == 2

    # Batch delete them
    delete_resp = client.post('/api/documents/batch_delete', json={'ids': doc_ids}, headers=headers)
    assert delete_resp.status_code == 200
    assert "Successfully deleted 2 documents" in delete_resp.get_json()['msg']

    # Verify they are gone
    list_after_delete = client.get('/api/documents', headers=headers)
    assert len(list_after_delete.get_json()) == 0
