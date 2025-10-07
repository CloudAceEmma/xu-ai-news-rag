import React, { useState, useEffect } from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Container from '@mui/material/Container';
import Header from './components/Common/Header';
import PrivateRoute from './components/Common/PrivateRoute';
import AuthPage from './pages/AuthPage';
import DashboardPage from './pages/DashboardPage';

const theme = createTheme();

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsLoggedIn(true);
    }
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Header isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} />
        <Container component="main" maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
          <Routes>
            <Route
              path="/auth"
              element={
                isLoggedIn ? (
                  <Navigate to="/dashboard" />
                ) : (
                  <AuthPage setIsLoggedIn={setIsLoggedIn} />
                )
              }
            />
            <Route
              path="/dashboard"
              element={
                <PrivateRoute isLoggedIn={isLoggedIn}>
                  <DashboardPage />
                </PrivateRoute>
              }
            />
            <Route
              path="*"
              element={<Navigate to={isLoggedIn ? '/dashboard' : '/auth'} />}
            />
          </Routes>
        </Container>
      </Router>
    </ThemeProvider>
  );
}

export default App;
