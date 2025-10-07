import React, { useState } from 'react';
import { TextField, Button, Box, Typography } from '@mui/material';
import apiClient from '../../api/axiosConfig';

const Login = ({ setIsLoggedIn }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await apiClient.post('/auth/login', {
        username,
        password,
      });
      localStorage.setItem('token', response.data.access_token);
      setIsLoggedIn(true);
    } catch (error) {
      setMessage(error.response.data.msg);
    }
  };

  return (
    <Box component="form" onSubmit={handleLogin} noValidate sx={{ mt: 1 }}>
      <TextField
        margin="normal"
        required
        fullWidth
        id="username"
        label="Username"
        name="username"
        autoComplete="username"
        autoFocus
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <TextField
        margin="normal"
        required
        fullWidth
        name="password"
        label="Password"
        type="password"
        id="password"
        autoComplete="current-password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <Button
        type="submit"
        fullWidth
        variant="contained"
        sx={{ mt: 3, mb: 2 }}
      >
        Sign In
      </Button>
      {message && <Typography color="error">{message}</Typography>}
    </Box>
  );
};

export default Login;
