import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import DocumentList from '../DocumentList';
import apiClient from '../../../api/axiosConfig';

jest.mock('../../../api/axiosConfig');

const mockDocuments = [
  { id: 1, file_path: 'test1.txt', document_type: 'txt', source: 'local', tags: 'test' },
  { id: 2, file_path: 'test2.pdf', document_type: 'pdf', source: 'web', tags: 'research' },
];

describe('DocumentList', () => {
  beforeEach(() => {
    apiClient.get.mockResolvedValue({ data: mockDocuments });
  });

  it('should fetch and display documents', async () => {
    render(<DocumentList />);
    await waitFor(() => {
      expect(screen.getByText('test1.txt')).toBeInTheDocument();
      expect(screen.getByText('test2.pdf')).toBeInTheDocument();
    });
  });

  it('should delete a document', async () => {
    apiClient.delete.mockResolvedValue({});
    render(<DocumentList />);
    await waitFor(() => {
      expect(screen.getByText('test1.txt')).toBeInTheDocument();
    });

    const deleteButtons = screen.getAllByLabelText(/delete/i);
    fireEvent.click(deleteButtons[0]);

    await waitFor(() => {
      expect(apiClient.delete).toHaveBeenCalledWith('/documents/1');
    });
  });

  it('should open edit form and update a document', async () => {
    apiClient.put.mockResolvedValue({});
    render(<DocumentList />);
    await waitFor(() => {
      expect(screen.getByText('test1.txt')).toBeInTheDocument();
    });

    const editButtons = screen.getAllByLabelText(/edit/i);
    fireEvent.click(editButtons[0]);

    await waitFor(() => {
      expect(screen.getByText('Edit Document 1')).toBeInTheDocument();
    });

    fireEvent.change(screen.getByLabelText(/source/i), { target: { value: 'updated source' } });
    fireEvent.change(screen.getByLabelText(/tags/i), { target: { value: 'updated,tags' } });
    fireEvent.click(screen.getByRole('button', { name: /update/i }));

    await waitFor(() => {
      expect(apiClient.put).toHaveBeenCalledWith('/documents/1', {
        source: 'updated source',
        tags: 'updated,tags',
      });
    });
  });
  
  it('should handle error when fetching documents', async () => {
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    apiClient.get.mockRejectedValue(new Error('Failed to fetch'));
    render(<DocumentList />);
    await waitFor(() => {
      expect(consoleErrorSpy).toHaveBeenCalledWith('Error fetching documents:', expect.any(Error));
    });
    consoleErrorSpy.mockRestore();
  });
});