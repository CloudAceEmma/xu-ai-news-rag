import React, { useState } from 'react';
import { Card, CardContent, Typography, TextField, Button, Box } from '@mui/material';
import apiClient from '../../api/axiosConfig';

const UploadForm = () => {
  const [file, setFile] = useState(null);
  const [source, setSource] = useState('');
  const [tags, setTags] = useState('');
  const [message, setMessage] = useState('');

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setMessage('Please select a file to upload.');
      return;
    }
    const formData = new FormData();
    formData.append('file', file);
    formData.append('source', source);
    formData.append('tags', tags);

    try {
      const response = await apiClient.post('/documents', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setMessage(response.data.msg);
    } catch (error) {
      if (error.response && error.response.data && error.response.data.msg) {
        setMessage(error.response.data.msg);
      } else {
        setMessage('An unexpected error occurred.');
      }
    }
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Upload Document
        </Typography>
        <Box component="form" onSubmit={handleUpload}>
          <TextField
            type="file"
            inputProps={{ 'aria-label': 'Upload Document', 'data-testid': 'file-input' }}
            onChange={(e) => setFile(e.target.files[0])}
            required
            fullWidth
            margin="normal"
          />
          <TextField
            label="Source"
            value={source}
            onChange={(e) => setSource(e.target.value)}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Tags (comma-separated)"
            value={tags}
            onChange={(e) => setTags(e.target.value)}
            fullWidth
            margin="normal"
          />
          <Button type="submit" variant="contained" sx={{ mt: 2 }}>
            Upload
          </Button>
        </Box>
        {message && <Typography sx={{ mt: 2 }}>{message}</Typography>}
      </CardContent>
    </Card>
  );
};

export default UploadForm;
