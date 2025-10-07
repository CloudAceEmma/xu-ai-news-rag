import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchBar from '../SearchBar';
import apiClient from '../../../api/axiosConfig';

jest.mock('../../../api/axiosConfig');

describe('SearchBar', () => {
  it('should return a search result', async () => {
    const result = {
      answer: 'This is a test answer.',
      source: 'Local Knowledge Base',
    };
    apiClient.post.mockResolvedValue({ data: result });

    render(<SearchBar />);

    fireEvent.change(screen.getByLabelText(/ask a question/i), {
      target: { value: 'test query' },
    });
    fireEvent.click(screen.getByRole('button', { name: /search/i }));

    await waitFor(() => {
      expect(apiClient.post).toHaveBeenCalledWith('/search', {
        query: 'test query',
      });
      expect(screen.getByText('This is a test answer.')).toBeInTheDocument();
      expect(
        screen.getByText('Source: Local Knowledge Base')
      ).toBeInTheDocument();
    });
  });
});
