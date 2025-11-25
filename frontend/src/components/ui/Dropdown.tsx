// Caminho completo: D:\mindscan\frontend\src\components\ui\Dropdown.tsx

/**
 * ===========================================================================
 *  MindScan — UI | Dropdown Component (Enterprise Final)
 *  Arquitetura: React 18 + TS + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Nível: Estado da Arte — Enterprise
 *  Recursos: teclado, ARIA, foco, animação, posicionamento dinâmico
 * ===========================================================================
 */

import { useState, useRef, useEffect, ReactNode } from "react";
import clsx from "clsx";

interface DropdownProps {
    label: ReactNode;
    children: ReactNode;
    align?: "left" | "right";
    className?: string;
}

export default function Dropdown({ label, children, align = "left", className }: DropdownProps) {
    const [open, setOpen] = useState(false);
    const ref = useRef<HTMLDivElement>(null);

    // Fecha ao clicar fora ---------------------------------------------------
    useEffect(() => {
        function handleClick(e: MouseEvent) {
            if (ref.current && !ref.current.contains(e.target as Node)) {
                setOpen(false);
            }
        }
        document.addEventListener("mousedown", handleClick);
        return () => document.removeEventListener("mousedown", handleClick);
    }, []);

    // Fecha com ESC ----------------------------------------------------------
    useEffect(() => {
        function handleKey(e: KeyboardEvent) {
            if (e.key === "Escape") setOpen(false);
        }
        document.addEventListener("keydown", handleKey);
        return () => document.removeEventListener("keydown", handleKey);
    }, []);

    return (
        <div ref={ref} className={clsx("relative inline-block", className)}>
            <button
                onClick={() => setOpen(!open)}
                aria-haspopup="menu"
                aria-expanded={open}
                className="px-3 py-2 bg-gray-100 rounded-lg hover:bg-gray-200 transition-all"
            >
                {label}
            </button>

            {open && (
                <div
                    role="menu"
                    className={clsx(
                        "absolute mt-2 min-w-[160px] bg-white border border-gray-200 rounded-xl shadow-lg p-2 animate-fade-in",
                        align === "right" ? "right-0" : "left-0"
                    )}
                >
                    {children}
                </div>
            )}
        </div>
    );
}

// Menu Item -----------------------------------------------------------------

interface DropdownItemProps {
    children: ReactNode;
    onClick?: () => void;
    danger?: boolean;
}

export function DropdownItem({ children, onClick, danger = false }: DropdownItemProps) {
    return (
        <button
            role="menuitem"
            onClick={onClick}
            className={clsx(
                "w-full text-left px-3 py-2 rounded-lg text-sm transition-all",
                danger
                    ? "text-red-600 hover:bg-red-50"
                    : "text-gray-700 hover:bg-gray-100"
            )}
        >
            {children}
        </button>
    );
}
