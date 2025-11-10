'use client';

import React, { useEffect, useState } from 'react';
import FormularioDASS21 from '@/components/forms/FormularioDASS21';
import { motion, AnimatePresence } from 'framer-motion';
import { Sun, Moon, CheckCircle, AlertCircle } from 'lucide-react';

export default function PaginaDASS21() {
  const [darkMode, setDarkMode] = useState(false);
  const [feedback, setFeedback] = useState<null | 'success' | 'error'>(null);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem('theme');
      if (stored === 'dark') {
        document.documentElement.classList.add('dark');
        setDarkMode(true);
      }
    }
  }, []);

  const toggleTheme = () => {
    const root = document.documentElement;
    const isDark = root.classList.toggle('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    setDarkMode(isDark);
  };

  return (
    <main className="min-h-screen bg-background text-foreground transition-colors duration-300">
      <header className="w-full py-6 border-b border-muted bg-white dark:bg-zinc-900 shadow-sm transition-colors duration-300">
        <div className="max-w-5xl mx-auto flex items-center justify-between px-4">
          <div className="flex items-center gap-4">
            <img src="/logo-synmind.png" alt="SynMind" className="h-10" />
            <h1 className="text-xl font-semibold tracking-tight">MindScan — Autoavaliação DASS-21</h1>
          </div>
          <button
            onClick={toggleTheme}
            className="p-2 rounded-full hover:bg-muted transition-colors"
            aria-label="Alternar modo de cor"
          >
            {darkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
          </button>
        </div>
      </header>

      <motion.section
        className="max-w-5xl mx-auto px-4 py-10"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <FormularioDASS21 setFeedback={setFeedback} />

        <AnimatePresence>
          {feedback === 'success' && (
            <motion.div
              className="mt-6 flex items-center justify-center gap-2 text-green-600 dark:text-green-400"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <CheckCircle className="h-5 w-5" /> Respostas enviadas com sucesso!
            </motion.div>
          )}
          {feedback === 'error' && (
            <motion.div
              className="mt-6 flex items-center justify-center gap-2 text-red-600 dark:text-red-400"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <AlertCircle className="h-5 w-5" /> Ocorreu um erro. Tente novamente.
            </motion.div>
          )}
        </AnimatePresence>
      </motion.section>

      <footer className="text-center text-sm text-muted-foreground py-6 transition-colors duration-300 dark:text-zinc-400">
        &copy; {new Date().getFullYear()} SynMind. Todos os direitos reservados.
      </footer>
    </main>
  );
}