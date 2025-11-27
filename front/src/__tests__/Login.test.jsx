import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import axios from 'axios';
import { MemoryRouter } from 'react-router-dom';
import Login from '../pages/Login';
import { AuthContext } from '../context/AuthContext';
import { vi } from 'vitest';

test('successful submit calls login from context', async () => {
  const mockLogin = vi.fn();
  axios.post = vi.fn().mockResolvedValue({ data: { token: 'abc' } });

  render(
    <AuthContext.Provider value={{ login: mockLogin, token: null, checked: true }}>
      <MemoryRouter>
        <Login />
      </MemoryRouter>
    </AuthContext.Provider>
  );

  fireEvent.change(screen.getByLabelText(/Usuário/i), { target: { value: 'admin' } });
  fireEvent.change(screen.getByLabelText(/Senha/i), { target: { value: 'secret' } });
  fireEvent.click(screen.getByRole('button', { name: /Entrar/i }));

  await waitFor(() => expect(axios.post).toHaveBeenCalledWith('/api/login', { username: 'admin', password: 'secret' }));
  await waitFor(() => expect(mockLogin).toHaveBeenCalledWith('abc'));
});
