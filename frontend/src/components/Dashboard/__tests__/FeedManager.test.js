import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import FeedManager from '../FeedManager';
import apiClient from '../../../api/axiosConfig';

jest.mock('../../../api/axiosConfig');

describe('FeedManager', () => {
  beforeEach(() => {
    apiClient.get.mockResolvedValue({ data: [] });
  });

  it('should render the component', () => {
    render(<FeedManager />);
    expect(screen.getByText('RSS Feeds')).toBeInTheDocument();
  });

  it('should add a new feed successfully', async () => {
    apiClient.post.mockResolvedValue({ data: { id: 2, url: 'http://new.com/rss' } });
    apiClient.get.mockResolvedValueOnce({ data: [{ id: 1, url: 'http://test.com/rss' }] })
                 .mockResolvedValueOnce({ data: [{ id: 1, url: 'http://test.com/rss' }, { id: 2, url: 'http://new.com/rss' }] });

    render(<FeedManager />);
    
    fireEvent.change(screen.getByLabelText(/rss feed url/i), {
      target: { value: 'http://new.com/rss' },
    });
    fireEvent.click(screen.getByRole('button', { name: /add/i }));

    await waitFor(() => {
      expect(apiClient.post).toHaveBeenCalledWith('/feeds', { url: 'http://new.com/rss' });
      expect(screen.getByText('http://new.com/rss')).toBeInTheDocument();
    });
  });

  it('should delete a feed successfully', async () => {
    apiClient.delete.mockResolvedValue({});
    apiClient.get.mockResolvedValueOnce({ data: [{ id: 1, url: 'http://test.com/rss' }] })
                 .mockResolvedValueOnce({ data: [] });

    await waitFor(() => {
        render(<FeedManager />);
    });
    expect(screen.getByText('http://test.com/rss')).toBeInTheDocument();

    fireEvent.click(screen.getByLabelText(/delete/i));

    await waitFor(() => {
      expect(apiClient.delete).toHaveBeenCalledWith('/feeds/1');
      expect(screen.queryByText('http://test.com/rss')).not.toBeInTheDocument();
    });
  });

  it('should handle error when adding a feed', async () => {
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    apiClient.post.mockRejectedValue(new Error('Failed to add feed'));

    render(<FeedManager />);

    fireEvent.change(screen.getByLabelText(/rss feed url/i), {
      target: { value: 'http://bad-url.com/rss' },
    });
    fireEvent.click(screen.getByRole('button', { name: /add/i }));

    await waitFor(() => {
      expect(consoleErrorSpy).toHaveBeenCalledWith('Error adding feed:', expect.any(Error));
    });
    consoleErrorSpy.mockRestore();
  });

  it('should handle error when deleting a feed', async () => {
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    apiClient.get.mockResolvedValue({ data: [{ id: 1, url: 'http://test.com/rss' }] });
    apiClient.delete.mockRejectedValue(new Error('Failed to delete feed'));

    render(<FeedManager />);
    
    await waitFor(() => {
        expect(screen.getByText('http://test.com/rss')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByLabelText(/delete/i));

    await waitFor(() => {
      expect(consoleErrorSpy).toHaveBeenCalledWith('Error deleting feed:', expect.any(Error));
    });
    consoleErrorSpy.mockRestore();
  });
});
