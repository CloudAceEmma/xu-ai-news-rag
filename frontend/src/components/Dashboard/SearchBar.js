import React, { useState } from 'react';
import {
  Card, CardContent, Typography, TextField, Button, Box, InputAdornment
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import apiClient from '../../api/axiosConfig';

const SearchBar = () => {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    try {
      const response = await apiClient.post('/search', { query });
      setResult(response.data);
    } catch (error) {
      console.error('Error searching:', error);
    }
  };

  return (
    <Card sx={{ mb: 3 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Search Knowledge Base
        </Typography>
        <Box component="form" onSubmit={handleSearch} sx={{ display: 'flex', alignItems: 'center' }}>
          <TextField
            fullWidth
            label="Ask a question..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            required
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
          />
          <Button type="submit" variant="contained" sx={{ ml: 2 }}>
            Search
          </Button>
        </Box>
        {result && (
          <Box sx={{ mt: 2 }}>
            <Typography variant="h6">Answer:</Typography>
            <Typography>{result.answer}</Typography>
            <Typography variant="caption" color="text.secondary">
              Source: {result.source}
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default SearchBar;
