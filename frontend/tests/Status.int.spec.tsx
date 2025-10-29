// Caminho completo: tests/Status.int.spec.tsx

import { render, screen, waitFor } from '@testing-library/react'
import Status from '../src/pages/Status'
import { MemoryRouter } from 'react-router-dom'

describe('[INT] Status - Integração com API mock', () => {
  it('exibe status do sistema corretamente', async () => {
    render(
      <MemoryRouter>
        <Status />
      </MemoryRouter>
    )

    await waitFor(() => {
      expect(screen.getByText(/status do sistema/i)).toBeInTheDocument()
      expect(screen.getByText(/api is up and running/i)).toBeInTheDocument()
    })
  })

  it('lida com falha na API simulada', async () => {
    // Simula erro no endpoint /status
    const { server } = await import('./mocks/server')
    const { rest } = await import('msw')

    server.use(
      rest.get('/status', (req, res, ctx) => {
        return res(
          ctx.status(500),
          ctx.json({ message: 'Erro simulado' })
        )
      })
    )

    render(
      <MemoryRouter>
        <Status />
      </MemoryRouter>
    )

    await waitFor(() => {
      expect(screen.getByText(/erro simulado/i)).toBeInTheDocument()
    })
  })
})