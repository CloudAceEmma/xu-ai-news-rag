import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import AuthPage from '../../pages/AuthPage';
import { BrowserRouter as Router } from 'react-router-dom';

describe('AuthPage', () => {
  it('should switch between login and register forms', () => {
    render(
      <Router>
        <AuthPage setIsLoggedIn={() => {}} />
      </Router>
    );

    // Starts on Login
    expect(screen.getByRole('heading', { name: /sign in/i })).toBeInTheDocument();
    
    // Switch to Register
    fireEvent.click(screen.getByText(/don't have an account\? sign up/i));
    expect(screen.getByRole('heading', { name: /sign up/i })).toBeInTheDocument();

    // Switch back to Login
    fireEvent.click(screen.getByText(/already have an account\? sign in/i));
    expect(screen.getByRole('heading', { name: /sign in/i })).toBeInTheDocument();
  });
});
