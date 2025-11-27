import React from 'react';
import { render, screen } from '@testing-library/react';
import axios from 'axios';
import { MemoryRouter } from 'react-router-dom';
import Profile from '../pages/Profile';
import { AuthContext } from '../context/AuthContext';
import { vi } from 'vitest';

test('loads and displays profile data', async () => {
  const mockData = {
    username: 'john',
    hostname: 'host1',
    session_id: 's1',
    login_time: '2025-01-01T12:00:00Z'
  };
  axios.get = vi.fn().mockResolvedValue({ data: mockData });
  const mockLogout = vi.fn();

  render(
    <AuthContext.Provider value={{ logout: mockLogout, token: 'abc' }}>
      <MemoryRouter>
        <Profile />
      </MemoryRouter>
    </AuthContext.Provider>
  );

  expect(await screen.findByText(/Bem-vindo, john/i)).toBeInTheDocument();
  expect(axios.get).toHaveBeenCalledWith('/api/profile', { headers: { Authorization: 'Bearer abc' } });
});
