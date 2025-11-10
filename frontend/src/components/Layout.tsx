import { ReactNode } from 'react';
import { Header } from './Header';

interface Props {
  children: ReactNode;
}

export function Layout({ children }: Props) {
  return (
    <div className="min-h-screen bg-gray-100 text-gray-900 dark:bg-gray-900 dark:text-white transition-colors">
      <Header />
      <main className="p-4 max-w-3xl mx-auto">{children}</main>
    </div>
  );
}
