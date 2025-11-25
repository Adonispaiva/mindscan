// Caminho completo: D:\mindscan\frontend\src\components\ui\Badge.tsx

/**
 * ===========================================================================
 *  MindScan — UI | Badge Component (Enterprise Final)
 *  Arquitetura: React 18 + TS + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Nível: Estado da Arte — Enterprise
 *  Recursos: Variantes avançadas, ícones opcionais, acessibilidade completa
 * ===========================================================================
 */

import { ReactNode } from "react";
import clsx from "clsx";

interface BadgeProps {
    children: ReactNode;
    variant?: "success" | "warning" | "info" | "danger" | "neutral";
    size?: "sm" | "md" | "lg";
    leftIcon?: ReactNode;
    rightIcon?: ReactNode;
    className?: string;
    role?: string;
}

const variantMap: Record<string, string> = {
    success: "bg-green-100 text-green-700 border border-green-300",
    warning: "bg-yellow-100 text-yellow-800 border border-yellow-300",
    info: "bg-blue-100 text-blue-700 border border-blue-300",
    danger: "bg-red-100 text-red-700 border border-red-300",
    neutral: "bg-gray-100 text-gray-700 border border-gray-300",
};

const sizeMap: Record<string, string> = {
    sm: "text-xs px-2 py-0.5",
    md: "text-sm px-3 py-1",
    lg: "text-base px-4 py-1.5",
};

export default function Badge({
    children,
    variant = "neutral",
    size = "md",
    leftIcon,
    rightIcon,
    className,
    role = "status",
}: BadgeProps) {
    return (
        <span
            role={role}
            className={clsx(
                "inline-flex items-center gap-1 font-medium rounded-full whitespace-nowrap select-none",
                variantMap[variant],
                sizeMap[size],
                className
            )}
        >
            {leftIcon && <span className="flex items-center text-current">{leftIcon}</span>}
            <span>{children}</span>
            {rightIcon && <span className="flex items-center text-current">{rightIcon}</span>}
        </span>
    );
}