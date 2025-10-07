import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Register from '../Register';
import apiClient from '../../../api/axiosConfig';

jest.mock('../../../api/axiosConfig');

describe('Register', () => {
  it('should register successfully', async () => {
    apiClient.post.mockResolvedValue({
      data: { msg: 'User created successfully' },
    });

    render(<Register />);

    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: 'testuser' },
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'password' },
    });
    fireEvent.click(screen.getByRole('button', { name: /sign up/i }));

    await waitFor(() => {
      expect(apiClient.post).toHaveBeenCalledWith('/auth/register', {
        username: 'testuser',
        password: 'password',
      });
      expect(screen.getByText('User created successfully')).toBeInTheDocument();
    });
  });
});
