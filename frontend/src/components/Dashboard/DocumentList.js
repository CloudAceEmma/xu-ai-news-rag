import React, { useState, useEffect } from 'react';
import {
  Card, CardContent, Typography, List, ListItem, ListItemText, IconButton,
  TextField, Button, Box
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import apiClient from '../../api/axiosConfig';

const DocumentList = () => {
  const [documents, setDocuments] = useState([]);
  const [editingDoc, setEditingDoc] = useState(null);
  const [source, setSource] = useState('');
  const [tags, setTags] = useState('');

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const response = await apiClient.get('/documents');
      setDocuments(response.data);
    } catch (error) {
      console.error('Error fetching documents:', error);
    }
  };

  const handleDelete = async (docId) => {
    try {
      await apiClient.delete(`/documents/${docId}`);
      fetchDocuments();
    } catch (error) {
      console.error('Error deleting document:', error);
    }
  };

  const handleEdit = (doc) => {
    setEditingDoc(doc);
    setSource(doc.source || '');
    setTags(doc.tags || '');
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      await apiClient.put(`/documents/${editingDoc.id}`, { source, tags });
      setEditingDoc(null);
      fetchDocuments();
    } catch (error) {
      console.error('Error updating document:', error);
    }
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Documents
        </Typography>
        <List>
          {documents.map((doc) => (
            <ListItem
              key={doc.id}
              secondaryAction={
                <>
                  <IconButton edge="end" aria-label="edit" onClick={() => handleEdit(doc)}>
                    <EditIcon />
                  </IconButton>
                  <IconButton edge="end" aria-label="delete" onClick={() => handleDelete(doc.id)}>
                    <DeleteIcon />
                  </IconButton>
                </>
              }
            >
              <ListItemText
                primary={doc.file_path}
                secondary={`Type: ${doc.document_type} | Source: ${doc.source} | Tags: ${doc.tags}`}
              />
            </ListItem>
          ))}
        </List>
        {editingDoc && (
          <Box component="form" onSubmit={handleUpdate} sx={{ mt: 2 }}>
            <Typography variant="h6">Edit Document {editingDoc.id}</Typography>
            <TextField
              label="Source"
              value={source}
              onChange={(e) => setSource(e.target.value)}
              fullWidth
              margin="normal"
            />
            <TextField
              label="Tags"
              value={tags}
              onChange={(e) => setTags(e.target.value)}
              fullWidth
              margin="normal"
            />
            <Button type="submit" variant="contained" sx={{ mr: 1 }}>Update</Button>
            <Button onClick={() => setEditingDoc(null)}>Cancel</Button>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default DocumentList;
