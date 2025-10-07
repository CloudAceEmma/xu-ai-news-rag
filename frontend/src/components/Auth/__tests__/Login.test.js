import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Login from '../Login';
import apiClient from '../../../api/axiosConfig';

jest.mock('../../../api/axiosConfig');

describe('Login', () => {
  it('should login successfully', async () => {
    const setIsLoggedIn = jest.fn();
    apiClient.post.mockResolvedValue({
      data: { access_token: 'test_token' },
    });

    render(<Login setIsLoggedIn={setIsLoggedIn} />);

    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: 'testuser' },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'password' },
    });
    fireEvent.click(screen.getByRole('button', { name: /sign in/i }));

    await waitFor(() => {
      expect(apiClient.post).toHaveBeenCalledWith('/auth/login', {
        username: 'testuser',
        password: 'password',
      });
      expect(localStorage.getItem('token')).toBe('test_token');
      expect(setIsLoggedIn).toHaveBeenCalledWith(true);
    });
  });
});
