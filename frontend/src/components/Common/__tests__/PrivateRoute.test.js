import React from 'react';
import { render } from '@testing-library/react';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import PrivateRoute from '../PrivateRoute';

describe('PrivateRoute', () => {
  it('should render children when logged in', () => {
    const { getByText } = render(
      <MemoryRouter initialEntries={['/private']}>
        <Routes>
          <Route path="/private" element={<PrivateRoute isLoggedIn={true}><div>Private Content</div></PrivateRoute>} />
        </Routes>
      </MemoryRouter>
    );
    expect(getByText('Private Content')).toBeInTheDocument();
  });

  it('should redirect to /auth when not logged in', () => {
    const { container } = render(
      <MemoryRouter initialEntries={['/private']}>
        <Routes>
          <Route path="/auth" element={<div>Auth Page</div>} />
          <Route path="/private" element={<PrivateRoute isLoggedIn={false}><div>Private Content</div></PrivateRoute>} />
        </Routes>
      </MemoryRouter>
    );
    expect(container.innerHTML).toContain('Auth Page');
  });
});
