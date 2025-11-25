// Caminho completo: D:\mindscan\frontend\src\components\ui\Button.tsx

/**
 * ===========================================================================
 *  MindScan — UI | Button Component (Enterprise Final)
 *  Arquitetura: React 18 + TS + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Nível: Estado da Arte — Enterprise
 * ===========================================================================
 */

import { ButtonHTMLAttributes, ReactNode } from "react";
import clsx from "clsx";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
    children: ReactNode;
    variant?:
        | "primary"
        | "secondary"
        | "danger"
        | "outline"
        | "ghost";
    size?: "sm" | "md" | "lg";
    loading?: boolean;
    leftIcon?: ReactNode;
    rightIcon?: ReactNode;
}

const baseStyles =
    "inline-flex items-center justify-center font-medium rounded-lg transition-all focus:outline-none focus:ring-2 disabled:opacity-50 disabled:cursor-not-allowed";

const variantStyles: Record<string, string> = {
    primary: "bg-indigo-600 text-white hover:bg-indigo-700 focus:ring-indigo-500",
    secondary: "bg-gray-200 text-gray-800 hover:bg-gray-300 focus:ring-gray-400",
    danger: "bg-red-600 text-white hover:bg-red-700 focus:ring-red-500",
    outline:
        "border border-gray-300 text-gray-800 hover:bg-gray-100 focus:ring-gray-400",
    ghost: "text-gray-800 hover:bg-gray-100 focus:ring-gray-300",
};

const sizeStyles: Record<string, string> = {
    sm: "px-3 py-1 text-sm",
    md: "px-4 py-2 text-base",
    lg: "px-5 py-3 text-lg",
};

export default function Button({
    children,
    variant = "primary",
    size = "md",
    loading = false,
    leftIcon,
    rightIcon,
    className,
    ...props
}: ButtonProps) {
    return (
        <button
            className={clsx(
                baseStyles,
                variantStyles[variant],
                sizeStyles[size],
                className
            )}
            disabled={loading || props.disabled}
            {...props}
        >
            {/* Loading Spinner */}
            {loading && (
                <span className="mr-2 inline-block h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></span>
            )}

            {/* Left Icon */}
            {leftIcon && <span className="mr-2 flex items-center">{leftIcon}</span>}

            {/* Label */}
            <span>{children}</span>

            {/* Right Icon */}
            {rightIcon && <span className="ml-2 flex items-center">{rightIcon}</span>}
        </button>
    );
}