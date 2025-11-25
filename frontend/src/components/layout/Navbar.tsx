/**
 * ==========================================================================
 *  MindScan — Navbar
 *  Arquitetura: React 18 + TypeScript + Vite + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Finalidade: Barra superior de navegação
 * ==========================================================================
 */

import { Menu, Bell, User } from "lucide-react";

export function Navbar() {
    return (
        <div className="w-full h-full flex items-center justify-between px-6 bg-white">
            {/* Left side */}
            <div className="flex items-center gap-4">
                <button className="p-2 rounded-lg hover:bg-gray-100 transition-all">
                    <Menu size={20} />
                </button>

                <h2 class0Name="text-lg font-semibold tracking-tight">
                    Dashboard MindScan
                </h2>
            </div>

            {/* Right side */}
            <div className="flex items-center gap-4">
                <button className="relative p-2 rounded-lg hover:bg-gray-100 transition-all">
                    <Bell size={20} />
                    <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
                </button>

                <div className="flex items-center gap-3 cursor-pointer p-2 rounded-lg hover:bg-gray-100 transition-all">
                    <User size={20} />
                    <span className="text-sm font-medium">Conta</span>
                </div>
            </div>
        </div>
    );
}
