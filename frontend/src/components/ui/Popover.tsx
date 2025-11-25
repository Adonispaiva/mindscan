// Caminho completo: D:\mindscan\frontend\src\components\ui\Popover.tsx

/**
 * ===========================================================================
 *  MindScan — UI | Popover Component (Enterprise Final)
 *  Arquitetura: React 18 + TS + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Nível: Estado da Arte — Enterprise
 *  Recursos: foco, ARIA, teclado, posicionamento, animação, overlay opcional
 * ===========================================================================
 */

import { ReactNode, useRef, useState, useEffect } from "react";
import clsx from "clsx";

interface PopoverProps {
    trigger: ReactNode;
    children: ReactNode;
    position?: "top" | "bottom" | "left" | "right";
    withOverlay?: boolean;
    className?: string;
}

export default function Popover({
    trigger,
    children,
    position = "bottom",
    withOverlay = false,
    className,
}: PopoverProps) {
    const [open, setOpen] = useState(false);
    const ref = useRef<HTMLDivElement>(null);

    // Clique fora -------------------------------------------------------------------
    useEffect(() => {
        function handleClick(e: MouseEvent) {
            if (ref.current && !ref.current.contains(e.target as Node)) {
                setOpen(false);
            }
        }
        document.addEventListener("mousedown", handleClick);
        return () => document.removeEventListener("mousedown", handleClick);
    }, []);

    // ESC para fechar ----------------------------------------------------------------
    useEffect(() => {
        function handleKey(e: KeyboardEvent) {
            if (e.key === "Escape") setOpen(false);
        }
        document.addEventListener("keydown", handleKey);
        return () => document.removeEventListener("keydown", handleKey);
    }, []);

    const posMap: Record<string, string> = {
        top: "bottom-full left-1/2 -translate-x-1/2 mb-2",
        bottom: "top-full left-1/2 -translate-x-1/2 mt-2",
        left: "right-full top-1/2 -translate-y-1/2 mr-2",
        right: "left-full top-1/2 -translate-y-1/2 ml-2",
    };

    return (
        <div className="relative inline-block" ref={ref}>
            {/* Trigger */}
            <button
                onClick={() => setOpen(!open)}
                aria-haspopup="dialog"
                aria-expanded={open}
                className="px-3 py-2 bg-gray-100 rounded-lg hover:bg-gray-200 transition-all"
            >
                {trigger}
            </button>

            {/* Overlay opcional */}
            {withOverlay && open && (
                <div className="fixed inset-0 bg-black/40 z-40 animate-fade-in"></div>
            )}

            {/* Popover */}
            {open && (
                <div
                    role="dialog"
                    aria-modal="false"
                    className={clsx(
                        "absolute z-50 min-w-[200px] bg-white border border-gray-200 rounded-xl shadow-lg p-4 animate-fade-in",
                        posMap[position],
                        className
                    )}
                >
                    {children}
                </div>
            )}
        </div>
    );
}