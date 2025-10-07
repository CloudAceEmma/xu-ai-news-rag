import React, { useState } from 'react';
import { Grid, Typography, Box, Tabs, Tab, Paper } from '@mui/material';
import DocumentList from '../components/Dashboard/DocumentList';
import FeedManager from '../components/Dashboard/FeedManager';
import Reports from '../components/Dashboard/Reports';
import SearchBar from '../components/Dashboard/SearchBar';
import UploadForm from '../components/Dashboard/UploadForm';

const DashboardPage = () => {
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const tabContentStyle = (index) => ({
    gridArea: '1 / 1',
    visibility: tabValue === index ? 'visible' : 'hidden',
  });

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Typography variant="h4" component="h1" gutterBottom>
          Dashboard
        </Typography>
      </Grid>
      <Grid item xs={12}>
        <SearchBar />
      </Grid>
      <Grid item xs={12}>
        <Paper>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs value={tabValue} onChange={handleTabChange} aria-label="dashboard tabs">
              <Tab label="Knowledge Base" id="dashboard-tab-0" />
              <Tab label="RSS Feeds" id="dashboard-tab-1" />
              <Tab label="Reports" id="dashboard-tab-2" />
            </Tabs>
          </Box>
          <Box sx={{ p: 3, display: 'grid' }}>
            <Box sx={tabContentStyle(0)}>
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <UploadForm />
                </Grid>
                <Grid item xs={12}>
                  <DocumentList />
                </Grid>
              </Grid>
            </Box>
            <Box sx={tabContentStyle(1)}>
              <FeedManager />
            </Box>
            <Box sx={tabContentStyle(2)}>
              <Reports />
            </Box>
          </Box>
        </Paper>
      </Grid>
    </Grid>
  );
};

export default DashboardPage;
