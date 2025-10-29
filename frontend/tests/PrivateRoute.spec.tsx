import { render, screen } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import PrivateRoute from '../src/components/PrivateRoute'
import { AuthContext } from '../src/contexts/AuthContext'

const DummyComponent = () => <div>Área Protegida</div>
const Login = () => <div>Tela de Login</div>

describe('PrivateRoute', () => {
  it('bloqueia acesso se não autenticado', () => {
    render(
      <AuthContext.Provider value={{ user: null, login: jest.fn(), logout: jest.fn() }}>
        <MemoryRouter initialEntries={['/protegido']}>
          <Routes>
            <Route path="/protegido" element={<PrivateRoute><DummyComponent /></PrivateRoute>} />
            <Route path="/login" element={<Login />} />
          </Routes>
        </MemoryRouter>
      </AuthContext.Provider>
    )
    expect(screen.getByText(/tela de login/i)).toBeInTheDocument()
  })

  it('permite acesso se autenticado', () => {
    render(
      <AuthContext.Provider value={{ user: { nome: 'Teste' }, login: jest.fn(), logout: jest.fn() }}>
        <MemoryRouter initialEntries={['/protegido']}>
          <Routes>
            <Route path="/protegido" element={<PrivateRoute><DummyComponent /></PrivateRoute>} />
          </Routes>
        </MemoryRouter>
      </AuthContext.Provider>
    )
    expect(screen.getByText(/área protegida/i)).toBeInTheDocument()
  })
})
