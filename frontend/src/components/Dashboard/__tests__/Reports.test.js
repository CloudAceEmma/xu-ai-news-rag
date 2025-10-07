import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Reports from '../Reports';
import apiClient from '../../../api/axiosConfig';

jest.mock('../../../api/axiosConfig');

describe('Reports', () => {
  it('should render the component', () => {
    render(<Reports />);
    expect(screen.getByText('Reports')).toBeInTheDocument();
  });

  it('should fetch and display keywords report', async () => {
    apiClient.get.mockResolvedValue({
      data: { top_keywords: ['ai', 'react', 'testing'] },
    });

    render(<Reports />);
    fireEvent.click(screen.getByRole('button', { name: /generate keywords report/i }));

    await waitFor(() => {
      expect(apiClient.get).toHaveBeenCalledWith('/report/keywords');
      expect(screen.getByText('Top 10 Keywords')).toBeInTheDocument();
      expect(screen.getByText('ai')).toBeInTheDocument();
      expect(screen.getByText('react')).toBeInTheDocument();
      expect(screen.getByText('testing')).toBeInTheDocument();
    });
  });

  it('should fetch and display clustering report', async () => {
    apiClient.get.mockResolvedValue({
      data: { 'Cluster 1': ['tech', 'code'], 'Cluster 2': ['news', 'updates'] },
    });

    render(<Reports />);
    fireEvent.click(screen.getByRole('button', { name: /generate clustering report/i }));

    await waitFor(() => {
      expect(apiClient.get).toHaveBeenCalledWith('/report/clustering');
      expect(screen.getByText('Document Clusters')).toBeInTheDocument();
      expect(screen.getByText('Cluster 1')).toBeInTheDocument();
      expect(screen.getByText('tech, code')).toBeInTheDocument();
      expect(screen.getByText('Cluster 2')).toBeInTheDocument();
      expect(screen.getByText('news, updates')).toBeInTheDocument();
    });
  });

  it('should handle error when fetching keywords report', async () => {
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    apiClient.get.mockRejectedValue(new Error('Failed to fetch keywords'));

    render(<Reports />);
    fireEvent.click(screen.getByRole('button', { name: /generate keywords report/i }));

    await waitFor(() => {
      expect(consoleErrorSpy).toHaveBeenCalledWith('Error fetching keywords report:', expect.any(Error));
    });
    consoleErrorSpy.mockRestore();
  });

  it('should handle error when fetching clustering report', async () => {
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    apiClient.get.mockRejectedValue(new Error('Failed to fetch clusters'));

    render(<Reports />);
    fireEvent.click(screen.getByRole('button', { name: /generate clustering report/i }));

    await waitFor(() => {
      expect(consoleErrorSpy).toHaveBeenCalledWith('Error fetching clustering report:', expect.any(Error));
    });
    consoleErrorSpy.mockRestore();
  });
});
