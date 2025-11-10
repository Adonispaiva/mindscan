// ===============================================================
//  CONFIGURAÇÃO: POSTCSS
//  Projeto: MindScan — SynMind MI v2.0
//  Autor: Leo Vinci (GPT Inovexa)
//  Data: 07/11/2025
//  Função: Pipeline CSS para Tailwind, Autoprefixer e Minify
// ===============================================================

export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
    cssnano:
      process.env.NODE_ENV === "production"
        ? {
            preset: [
              "default",
              {
                discardComments: { removeAll: true },
                normalizeWhitespace: true,
              },
            ],
          }
        : false,
  },
};
