import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import UploadForm from '../UploadForm';
import apiClient from '../../../api/axiosConfig';

jest.mock('../../../api/axiosConfig');

describe('UploadForm', () => {
  it('should update form fields on change', () => {
    render(<UploadForm />);
    
    const sourceInput = screen.getByLabelText(/source/i);
    const tagsInput = screen.getByLabelText(/tags/i);

    fireEvent.change(sourceInput, { target: { value: 'TestSource' } });
    fireEvent.change(tagsInput, { target: { value: 'Test,Tags' } });

    expect(sourceInput.value).toBe('TestSource');
    expect(tagsInput.value).toBe('Test,Tags');
  });

  it('should show success message on successful upload', async () => {
    apiClient.post.mockResolvedValue({
      data: { msg: 'File uploaded successfully' },
    });

    render(<UploadForm />);

    const file = new File(['dummy content'], 'test.txt', { type: 'text/plain' });
    const fileInput = screen.getByTestId('file-input');
    const sourceInput = screen.getByLabelText(/source/i);
    const tagsInput = screen.getByLabelText(/tags/i);
    const uploadButton = screen.getByRole('button', { name: /upload/i });

    fireEvent.change(fileInput, { target: { files: [file] } });
    fireEvent.change(sourceInput, { target: { value: 'TestSource' } });
    fireEvent.change(tagsInput, { target: { value: 'Test,Tags' } });
    
    fireEvent.submit(uploadButton);

    await waitFor(() => {
      expect(apiClient.post).toHaveBeenCalledWith(
        '/documents',
        expect.any(FormData),
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );
      expect(screen.getByText('File uploaded successfully')).toBeInTheDocument();
    });
  });

  it('should show error message on failed upload', async () => {
    apiClient.post.mockRejectedValue({
      response: { data: { msg: 'Upload failed' } },
    });

    render(<UploadForm />);

    const file = new File(['dummy content'], 'test.txt', { type: 'text/plain' });
    const fileInput = screen.getByTestId('file-input');
    const uploadButton = screen.getByRole('button', { name: /upload/i });

    fireEvent.change(fileInput, { target: { files: [file] } });
    fireEvent.submit(uploadButton);

    await waitFor(() => {
      expect(screen.getByText('Upload failed')).toBeInTheDocument();
    });
  });

  it('should show a message if no file is selected', async () => {
    render(<UploadForm />);
    const uploadButton = screen.getByRole('button', { name: /upload/i });
    fireEvent.click(uploadButton);
    
    await waitFor(() => {
        expect(screen.getByText('Please select a file to upload.')).toBeInTheDocument();
    });
  });
});
