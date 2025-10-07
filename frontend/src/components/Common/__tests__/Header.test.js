import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Header from '../Header';

describe('Header', () => {
  it('should render logout button when logged in', () => {
    render(<Header isLoggedIn={true} setIsLoggedIn={() => {}} />);
    expect(screen.getByRole('button', { name: /logout/i })).toBeInTheDocument();
  });

  it('should not render logout button when not logged in', () => {
    render(<Header isLoggedIn={false} setIsLoggedIn={() => {}} />);
    expect(screen.queryByRole('button', { name: /logout/i })).not.toBeInTheDocument();
  });

  it('should call setIsLoggedIn on logout', () => {
    const setIsLoggedIn = jest.fn();
    render(<Header isLoggedIn={true} setIsLoggedIn={setIsLoggedIn} />);
    fireEvent.click(screen.getByRole('button', { name: /logout/i }));
    expect(setIsLoggedIn).toHaveBeenCalledWith(false);
  });
});
