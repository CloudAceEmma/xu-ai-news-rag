import React, { useState } from 'react';
import { TextField, Button, Box, Typography } from '@mui/material';
import apiClient from '../../api/axiosConfig';

const Register = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const response = await apiClient.post('/auth/register', {
        username,
        password,
      });
      setMessage(response.data.msg);
    } catch (error) {
      setMessage(error.response.data.msg);
    }
  };

  return (
    <Box component="form" onSubmit={handleRegister} noValidate sx={{ mt: 1 }}>
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
        autoComplete="new-password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <Button
        type="submit"
        fullWidth
        variant="contained"
        sx={{ mt: 3, mb: 2 }}
      >
        Sign Up
      </Button>
      {message && <Typography color={message.includes('successfully') ? 'primary' : 'error'}>{message}</Typography>}
    </Box>
  );
};

export default Register;
