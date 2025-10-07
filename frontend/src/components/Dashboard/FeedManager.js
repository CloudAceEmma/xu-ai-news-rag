import React, { useState, useEffect } from 'react';
import {
  Card, CardContent, Typography, List, ListItem, ListItemText, IconButton,
  TextField, Button, Box
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import apiClient from '../../api/axiosConfig';

const FeedManager = () => {
  const [feeds, setFeeds] = useState([]);
  const [url, setUrl] = useState('');

  useEffect(() => {
    fetchFeeds();
  }, []);

  const fetchFeeds = async () => {
    try {
      const response = await apiClient.get('/feeds');
      setFeeds(response.data);
    } catch (error) {
      console.error('Error fetching feeds:', error);
    }
  };

  const handleAddFeed = async (e) => {
    e.preventDefault();
    try {
      await apiClient.post('/feeds', { url });
      setUrl('');
      fetchFeeds();
    } catch (error) {
      console.error('Error adding feed:', error);
    }
  };

  const handleDeleteFeed = async (feedId) => {
    try {
      await apiClient.delete(`/feeds/${feedId}`);
      fetchFeeds();
    } catch (error) {
      console.error('Error deleting feed:', error);
    }
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          RSS Feeds
        </Typography>
        <Box component="form" onSubmit={handleAddFeed} sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <TextField
            fullWidth
            label="RSS Feed URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            required
          />
          <Button type="submit" variant="contained" sx={{ ml: 2 }}>
            Add
          </Button>
        </Box>
        <List>
          {feeds.map((feed) => (
            <ListItem
              key={feed.id}
              secondaryAction={
                <IconButton edge="end" aria-label="delete" onClick={() => handleDeleteFeed(feed.id)}>
                  <DeleteIcon />
                </IconButton>
              }
            >
              <ListItemText primary={feed.url} />
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export default FeedManager;
