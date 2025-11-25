/**
 * ===========================================================================
 *  MindScan — UI | Tooltip Component (Enterprise Final)
 *  Arquitetura: React 18 + TS + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Nível: Estado da Arte — Enterprise
 *  Recursos: posição dinâmica, delay, ARIA, animação, hover/focus
 * ===========================================================================
 */

import { ReactNode, useState, useRef, useEffect } from "react";
import clsx from "clsx";

interface TooltipProps {
    children: ReactNode;
    label: ReactNode;
    position?: "top" | "bottom" | "left" | "right";
    delay?: number;
    className?: string;
}

export default function Tooltip({
    children,
    label,
    position = "top",
    delay = 200,
    className,
}: TooltipProps) {
    const [visible, setVisible] = useState(false);
    const timeoutRef = useRef<number>();

    const show = () => {
        timeoutRef.current = window.setTimeout(() => setVisible(true), delay);
    };

    const hide = () => {
        clearTimeout(timeoutRef.current);
        setVisible(false);
    };

    const positionMap: Record<string, string> = {
        top: "bottom-full left-1/2 -translate-x-1/2 mb-2",
        bottom: "top-full left-1/2 -translate-x-1/2 mt-2",
        left: "right-full top-1/2 -translate-y-1/2 mr-2",
        right: "left-full top-1/2 -translate-y-1/2 ml-2",
    };

    return (
        <div
            className={clsx("relative inline-block", className)}
            onMouseEnter={show}
            onMouseLeave={hide}
            onFocus={show}
            onBlur={hide}
        >
            {children}

            {visible && (
                <div
                    role="tooltip"
                    className={clsx(
                        "absolute z-50 px-3 py-2 text-xs rounded-lg bg-gray-900 text-white shadow-lg whitespace-nowrap animate-fade-in",
                        positionMap[position]
                    )}
                >
                    {label}
                </div>
            )}
        </div>
    );
}
