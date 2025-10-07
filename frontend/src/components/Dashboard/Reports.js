import React, { useState } from 'react';
import {
  Card, CardContent, Typography, Button, Box, Grid, List, ListItem, ListItemText
} from '@mui/material';
import apiClient from '../../api/axiosConfig';

const Reports = () => {
  const [keywords, setKeywords] = useState([]);
  const [clusters, setClusters] = useState(null);

  const fetchKeywords = async () => {
    try {
      const response = await apiClient.get('/report/keywords');
      setKeywords(response.data.top_keywords || []);
    } catch (error) {
      console.error('Error fetching keywords report:', error);
    }
  };

  const fetchClusters = async () => {
    try {
      const response = await apiClient.get('/report/clustering');
      setClusters(response.data);
    } catch (error) {
      console.error('Error fetching clustering report:', error);
    }
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Reports
        </Typography>
        <Box sx={{ mb: 2 }}>
          <Button variant="contained" onClick={fetchKeywords} sx={{ mr: 1 }}>
            Generate Keywords Report
          </Button>
          <Button variant="contained" onClick={fetchClusters}>
            Generate Clustering Report
          </Button>
        </Box>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            {keywords.length > 0 && (
              <Box>
                <Typography variant="h6">Top 10 Keywords</Typography>
                <List>
                  {keywords.map((keyword, index) => (
                    <ListItem key={index}>
                      <ListItemText primary={keyword} />
                    </ListItem>
                  ))}
                </List>
              </Box>
            )}
          </Grid>
          <Grid item xs={12} md={6}>
            {clusters && (
              <Box>
                <Typography variant="h6">Document Clusters</Typography>
                {clusters.error ? (
                  <Typography color="error">{clusters.error}</Typography>
                ) : (
                  Object.entries(clusters).map(([clusterName, terms]) => (
                    <Box key={clusterName} sx={{ mb: 1 }}>
                      <Typography variant="subtitle1">{clusterName}</Typography>
                      <Typography variant="body2">{terms.join(', ')}</Typography>
                    </Box>
                  ))
                )}
              </Box>
            )}
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default Reports;
