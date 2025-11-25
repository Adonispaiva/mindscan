// Caminho completo: D:\mindscan\frontend\src\components\ui\Sidebar.tsx

/**
 * ===========================================================================
 *  MindScan — UI | Sidebar Component (Enterprise Final)
 *  Arquitetura: React 18 + TS + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Nível: Estado da Arte — Enterprise
 *  Recursos: Navegação dinâmica, ícones, colapsável, ARIA, keyboard-nav
 * ===========================================================================
 */

import { ReactNode, useState } from "react";
import { NavLink } from "react-router-dom";
import clsx from "clsx";

interface SidebarItem {
    label: string;
    to: string;
    icon?: ReactNode;
}

interface SidebarProps {
    items: SidebarItem[];
    footer?: ReactNode;
    collapsible?: boolean;
}

export default function Sidebar({ items, footer, collapsible = true }: SidebarProps) {
    const [collapsed, setCollapsed] = useState(false);

    return (
        <aside
            className={clsx(
                "h-screen border-r border-gray-200 bg-white shadow-sm flex flex-col transition-all", 
                collapsed ? "w-20" : "w-64"
            )}
            role="navigation"
            aria-label="Menu lateral"
        >
            {/* Header */}
            <div className="p-4 flex justify-between items-center border-b border-gray-200">
                <span className="font-semibold text-lg tracking-tight truncate">
                    {collapsed ? "MS" : "MindScan"}
                </span>
                {collapsible && (
                    <button
                        aria-label={collapsed ? "Expandir menu" : "Colapsar menu"}
                        onClick={() => setCollapsed(!collapsed)}
                        className="p-2 rounded-lg hover:bg-gray-100"
                    >
                        {collapsed ? "➡" : "⬅"}
                    </button>
                )}
            </div>

            {/* Menu */}
            <nav className="flex-1 overflow-y-auto">
                <ul className="flex flex-col py-3">
                    {items.map((item) => (
                        <li key={item.to}>
                            <NavLink
                                to={item.to}
                                className={({ isActive }) =>
                                    clsx(
                                        "flex items-center gap-3 px-4 py-3 transition-colors",
                                        isActive
                                            ? "bg-indigo-50 text-indigo-600 font-semibold border-l-4 border-indigo-600"
                                            : "text-gray-700 hover:bg-gray-100 border-l-4 border-transparent"
                                    )
                                }
                            >
                                {item.icon && <span className="text-xl">{item.icon}</span>}
                                {!collapsed && <span className="truncate">{item.label}</span>}
                            </NavLink>
                        </li>
                    ))}
                </ul>
            </nav>

            {/* Footer */}
            {footer && (
                <div className="p-4 border-t border-gray-200 text-sm text-gray-600">
                    {footer}
                </div>
            )}
        </aside>
    );
}