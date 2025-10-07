import React, { useState } from 'react';
import { Container, Box, Paper, Typography, Button, Link } from '@mui/material';
import Login from '../components/Auth/Login';
import Register from '../components/Auth/Register';

const AuthPage = ({ setIsLoggedIn }) => {
  const [showLogin, setShowLogin] = useState(true);

  return (
    <Container component="main" maxWidth="xs">
      <Paper elevation={3} sx={{ p: 4, mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Typography component="h1" variant="h5">
          {showLogin ? 'Sign in' : 'Sign up'}
        </Typography>
        <Box sx={{ mt: 1 }}>
          {showLogin ? (
            <Login setIsLoggedIn={setIsLoggedIn} />
          ) : (
            <Register />
          )}
          <Link href="#" variant="body2" onClick={(e) => { e.preventDefault(); setShowLogin(!showLogin); }}>
            {showLogin ? "Don't have an account? Sign Up" : "Already have an account? Sign in"}
          </Link>
        </Box>
      </Paper>
    </Container>
  );
};

export default AuthPage;
