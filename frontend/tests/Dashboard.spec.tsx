import { render, screen } from '@testing-library/react'
import Dashboard from '../src/pages/Dashboard'
import { AuthContext } from '../src/contexts/AuthContext'
import { MemoryRouter } from 'react-router-dom'

describe('Dashboard Page', () => {
  it('renderiza saudação ao usuário autenticado', () => {
    const fakeUser = { nome: 'Leo Vinci' }

    render(
      <AuthContext.Provider value={{ user: fakeUser, login: jest.fn(), logout: jest.fn() }}>
        <MemoryRouter>
          <Dashboard />
        </MemoryRouter>
      </AuthContext.Provider>
    )

    expect(screen.getByText(/leo vinci/i)).toBeInTheDocument()
    expect(screen.getByText(/bem-vindo/i)).toBeInTheDocument()
  })
})
