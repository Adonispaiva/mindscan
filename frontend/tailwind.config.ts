// ===============================================================
//  CONFIGURAÇÃO: TAILWIND CSS
//  Projeto: MindScan — SynMind MI v2.0
//  Autor: Leo Vinci (GPT Inovexa)
//  Data: 07/11/2025
//  Função: Tema visual padrão Inovexa + SynMind
// ===============================================================

import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./index.html",
    "./src/**/*.{ts,tsx,js,jsx}",
    "./src/components/**/*.{ts,tsx}",
    "./src/pages/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Paleta Inovexa (Dark Corporate)
        inovexa: {
          50: "#f5f6ff",
          100: "#e1e4ff",
          200: "#bfc3ff",
          300: "#9ba0ff",
          400: "#7d82ff",
          500: "#5b63ff",
          600: "#434edb",
          700: "#343ca9",
          800: "#272b7d",
          900: "#1b1e57",
        },
        // Paleta SynMind (Inteligência & Calma)
        synmind: {
          50: "#eaf7ff",
          100: "#cbeaff",
          200: "#99d4ff",
          300: "#66bbff",
          400: "#339eff",
          500: "#1d84e6",
          600: "#1569b4",
          700: "#0f4e82",
          800: "#093351",
          900: "#041929",
        },
        slate: {
          950: "#0a0a12",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        display: ["Poppins", "Inter", "sans-serif"],
      },
      boxShadow: {
        glow: "0 0 12px rgba(93, 63, 211, 0.3)",
      },
      backgroundImage: {
        "grid-dark": "radial-gradient(rgba(255,255,255,0.05) 1px, transparent 1px)",
      },
      backgroundSize: {
        "grid-dark": "20px 20px",
      },
    },
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("tailwindcss-animate"),
  ],
};

export default config;
