// Caminho completo: D:\mindscan\frontend\src\components\ui\Navbar.tsx

/**
 * ===========================================================================
 *  MindScan — UI | Navbar Component (Enterprise Final)
 *  Arquitetura: React 18 + TS + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Nível: Estado da Arte — Enterprise
 *  Recursos: Acessibilidade, navegação, menu do usuário, slots, ícones
 * ===========================================================================
 */

import { ReactNode } from "react";
import { NavLink } from "react-router-dom";
import clsx from "clsx";

interface NavItem {
    label: string;
    to: string;
}

interface NavbarProps {
    items: NavItem[];
    rightSlot?: ReactNode;
}

export default function Navbar({ items, rightSlot }: NavbarProps) {
    return (
        <header
            className="w-full h-16 border-b border-gray-200 bg-white shadow-sm flex items-center px-6 justify-between"
            role="navigation"
            aria-label="Barra de navegação superior"
        >
            {/* Logo */}
            <div className="text-xl font-semibold tracking-tight">MindScan</div>

            {/* Menu */}
            <nav className="flex items-center gap-6">
                {items.map((item) => (
                    <NavLink
                        key={item.to}
                        to={item.to}
                        className={({ isActive }) =>
                            clsx(
                                "text-sm font-medium transition-colors",
                                isActive
                                    ? "text-indigo-600 border-b-2 border-indigo-600 pb-1"
                                    : "text-gray-700 hover:text-indigo-600"
                            )
                        }
                    >
                        {item.label}
                    </NavLink>
                ))}
            </nav>

            {/* Right Slot (user menu, actions, etc.) */}
            <div className="flex items-center gap-4">{rightSlot}</div>
        </header>
    );
}