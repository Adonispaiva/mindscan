import '@testing-library/jest-dom';
import { server } from './mocks/server';

// Inicia o MSW antes de todos os testes
beforeAll(() => server.listen());

// Reseta os handlers após cada teste
afterEach(() => server.resetHandlers());

// Encerra o servidor após todos os testes
afterAll(() => server.close());
