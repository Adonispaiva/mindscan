import { ThemeToggle } from './ThemeToggle';

export function Header() {
  return (
    <header className="bg-blue-600 text-white p-4 shadow-md rounded-b-2xl">
      <div className="max-w-3xl mx-auto flex items-center justify-between">
        <h1 className="text-xl font-bold">MindScan</h1>
        <div className="flex gap-2 items-center">
          <span className="text-sm opacity-80">SynMind</span>
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}
