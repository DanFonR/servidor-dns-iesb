import React, { useContext } from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { AuthProvider, AuthContext } from '../context/AuthContext';

test('login and logout update token and localStorage', async () => {
  localStorage.removeItem('token');

  const Consumer = () => {
    const { token, login, logout } = useContext(AuthContext);
    return (
      <div>
        <div data-testid="token">token:{token || ''}</div>
        <button onClick={() => login('tok')}>doLogin</button>
        <button onClick={() => logout()}>doLogout</button>
      </div>
    );
  };

  render(
    <MemoryRouter>
      <AuthProvider>
        <Consumer />
      </AuthProvider>
    </MemoryRouter>
  );

  expect(screen.getByTestId('token').textContent).toBe('token:');
  fireEvent.click(screen.getByText('doLogin'));
  await waitFor(() => expect(localStorage.getItem('token')).toBe('tok'));
  expect(screen.getByTestId('token').textContent).toBe('token:tok');
  fireEvent.click(screen.getByText('doLogout'));
  await waitFor(() => expect(localStorage.getItem('token')).toBeNull());
});
