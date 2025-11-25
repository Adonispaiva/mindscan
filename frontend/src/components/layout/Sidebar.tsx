/**
 * ==========================================================================
 *  MindScan — Sidebar
 *  Arquitetura: React 18 + TS + Vite + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Finalidade: Navegação lateral principal do sistema
 * ==========================================================================
 */

import { NavLink } from "react-router-dom";
import { useState } from "react";
import {
    Home,
    LayoutDashboard,
    Users,
    FileText,
    Settings,
    FileCheck,
    LogOut
} from "lucide-react";

interface NavItem {
    label: string;
    to: string;
    icon: React.ElementType;
}

const navItems: NavItem[] = [
    { label: "Home", to: "/", icon: Home },
    { label: "Dashboard", to: "/dashboard", icon: LayoutDashboard },
    { label: "Testes", to: "/tests", icon: FileCheck },
    { label: "Candidatos", to: "/candidates", icon: Users },
    { label: "Relatórios", to: "/reports", icon: FileText },
    { label: "Configurações", to: "/settings", icon: Settings }
];

export function Sidebar() {
    const [active, setActive] = useState<string>("");

    return (
        <div className="flex flex-col h-full py-6 px-4">
            {/* Logo */}
            <div className="mb-10">
                <h1 className="text-xl font-semibold tracking-tight">MindScan</h1>
                <p className="text-sm text-gray-500">SynMind Diagnostic System</p>
            </div>

            {/* Navigation */}
            <nav className="flex flex-col gap-2">
                {navItems.map(({ label, to, icon: Icon }) => (
                    <NavLink
                        key={label}
                        to={to}
                        onClick={() => setActive(label)}
                        className={({ isActive }) =>
                            `flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-all
                            ${
                                isActive || active === label
                                    ? "bg-indigo-100 text-indigo-700"
                                    : "text-gray-700 hover:bg-gray-100"
                            }`
                        }
                    >
                        <Icon size={18} />
                        {label}
                    </NavLink>
                ))}
            </nav>

            {/* Logout */}
            <div className="mt-auto pt-6 border-t border-gray-200">
                <button className="flex items-center gap-3 w-full px-3 py-2 rounded-lg text-sm text-red-600 hover:bg-red-50 transition-all">
                    <LogOut size={18} />
                    Sair
                </button>
            </div>
        </div>
    );
}
