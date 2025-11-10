import { render, screen } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import App from '../src/App'
import Login from '../src/pages/Login'
import NotFound from '../src/pages/NotFound'
import Dashboard from '../src/pages/Dashboard'
import { AuthProvider } from '../src/contexts/AuthContext'

describe('Testes de Rotas', () => {
  it('renderiza 404 para rota inexistente', () => {
    render(
      <MemoryRouter initialEntries={['/rota-inexistente']}>
        <App />
      </MemoryRouter>
    )
    expect(screen.getByText(/página não encontrada/i)).toBeInTheDocument()
  })

  it('renderiza a página de login corretamente', () => {
    render(
      <MemoryRouter initialEntries={['/login']}>
        <App />
      </MemoryRouter>
    )
    expect(screen.getByLabelText(/usuário/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /entrar/i })).toBeInTheDocument()
  })

  it('redireciona rota protegida se não autenticado', () => {
    render(
      <AuthProvider>
        <MemoryRouter initialEntries={['/dashboard']}>
          <Routes>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/login" element={<Login />} />
          </Routes>
        </MemoryRouter>
      </AuthProvider>
    )
    expect(screen.getByLabelText(/usuário/i)).toBeInTheDocument()
  })
})
