// Caminho completo: tests/Login.int.spec.tsx

import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import Login from '../src/pages/Login'
import { AuthContext } from '../src/contexts/AuthContext'
import { MemoryRouter } from 'react-router-dom'

describe('[INT] Login - Integração com API mock', () => {
  it('efetua login com credenciais válidas', async () => {
    const mockLogin = jest.fn()

    render(
      <AuthContext.Provider value={{ user: null, login: mockLogin, logout: jest.fn() }}>
        <MemoryRouter>
          <Login />
        </MemoryRouter>
      </AuthContext.Provider>
    )

    fireEvent.change(screen.getByLabelText(/usuário/i), {
      target: { value: 'admin' },
    })
    fireEvent.change(screen.getByLabelText(/senha/i), {
      target: { value: '1234' },
    })
    fireEvent.click(screen.getByRole('button', { name: /entrar/i }))

    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith('admin', '1234')
    })
  })

  it('exibe erro com credenciais inválidas', async () => {
    const mockLogin = jest.fn(() => {
      throw new Error('Credenciais inválidas')
    })

    render(
      <AuthContext.Provider value={{ user: null, login: mockLogin, logout: jest.fn() }}>
        <MemoryRouter>
          <Login />
        </MemoryRouter>
      </AuthContext.Provider>
    )

    fireEvent.change(screen.getByLabelText(/usuário/i), {
      target: { value: 'usuario-falso' },
    })
    fireEvent.change(screen.getByLabelText(/senha/i), {
      target: { value: 'errada' },
    })
    fireEvent.click(screen.getByRole('button', { name: /entrar/i }))

    await waitFor(() => {
      expect(screen.getByText(/credenciais inválidas/i)).toBeInTheDocument()
    })
  })
})
