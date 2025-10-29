import { render, screen } from '@testing-library/react'
import Status from '../src/pages/Status'

describe('Status Page', () => {
  it('renderiza corretamente o componente Status', () => {
    render(<Status />)

    expect(screen.getByText(/status do sistema/i)).toBeInTheDocument()
    expect(screen.getByText(/tudo funcionando/i)).toBeInTheDocument()
  })
})
