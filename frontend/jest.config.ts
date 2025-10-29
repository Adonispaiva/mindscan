import type { Config } from 'jest';

const config: Config = {
  // Define o preset TypeScript
  preset: 'ts-jest',

  // Define o ambiente de teste (DOM simulado)
  testEnvironment: 'jsdom',

  // Arquivo de inicialização do ambiente de teste (setup global)
  setupFilesAfterEnv: ['<rootDir>/tests/setupTests.ts'],

  // Define transformações (necessário para TypeScript e JSX)
  transform: {
    '^.+\\.tsx?$': 'ts-jest',
  },

  // Mapeamento de imports (para CSS modules e outros arquivos estáticos)
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
  },

  // Define o padrão de busca dos arquivos de teste
  testMatch: [
    '**/tests/**/*.spec.ts?(x)',
    '**/__tests__/**/*.spec.ts?(x)',
    '**/?(*.)+(spec|test).[tj]s?(x)',
  ],

  // Extensões reconhecidas
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],

  // Configura a coleta de cobertura de código
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'clover'],

  // Ignora diretórios que não devem ser testados
  testPathIgnorePatterns: ['/node_modules/', '/dist/', '/build/'],

  // Define verbose para mostrar resultados detalhados
  verbose: true,
};

export default config;
