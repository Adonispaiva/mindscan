// Caminho completo: tests/mocks/handlers.ts

import { rest } from 'msw'

export const handlers = [
  // Simula login com sucesso
  rest.post('/login', async (req, res, ctx) => {
    const { username } = await req.json()
    if (username === 'admin') {
      return res(
        ctx.status(200),
        ctx.json({ token: 'fake_token_12345' })
      )
    }
    return res(
      ctx.status(401),
      ctx.json({ message: 'Credenciais inválidas' })
    )
  }),

  // Simula recuperação de status
  rest.get('/status', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({ status: 'ok', uptime: 123456 })
    )
  }),

  // Simula erro no servidor
  rest.get('/error', (req, res, ctx) => {
    return res(
      ctx.status(500),
      ctx.json({ message: 'Erro interno no servidor' })
    )
  }),

  // Simula atraso
  rest.get('/delay', (req, res, ctx) => {
    return res(
      ctx.delay(1500),
      ctx.status(200),
      ctx.json({ delayed: true })
    )
  }),
]