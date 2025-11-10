import { render, screen, fireEvent } from '@testing-library/react'
import Login from '../src/pages/Login'
import { AuthContext } from '../src/contexts/AuthContext'
import { MemoryRouter } from 'react-router-dom'

describe('Login Page', () => {
  it('permite preencher e submeter o formulário de login', () => {
    const mockLogin = jest.fn()
    render(
      <AuthContext.Provider value={{ user: null, login: mockLogin, logout: jest.fn() }}>
        <MemoryRouter>
          <Login />
        </MemoryRouter>
      </AuthContext.Provider>
    )

    const userInput = screen.getByLabelText(/usuário/i)
    const passInput = screen.getByLabelText(/senha/i)
    const button = screen.getByRole('button', { name: /entrar/i })

    fireEvent.change(userInput, { target: { value: 'inovexa' } })
    fireEvent.change(passInput, { target: { value: '1234' } })
    fireEvent.click(button)

    expect(mockLogin).toHaveBeenCalledWith('inovexa', '1234')
  })

  it('exibe mensagem de erro se login falhar', () => {
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

    fireEvent.change(screen.getByLabelText(/usuário/i), { target: { value: 'errado' } })
    fireEvent.change(screen.getByLabelText(/senha/i), { target: { value: '0000' } })
    fireEvent.click(screen.getByRole('button', { name: /entrar/i }))

    expect(screen.findByText(/credenciais inválidas/i)).resolves.toBeTruthy()
  })
})
{\rtf1}