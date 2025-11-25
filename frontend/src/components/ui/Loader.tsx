// Caminho completo: D:\mindscan\frontend\src\components\ui\Loader.tsx

/**
 * ===========================================================================
 *  MindScan — UI | Loader Component (Enterprise Final)
 *  Arquitetura: React 18 + TS + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Nível: Estado da Arte — Enterprise
 *  Recursos: Variantes, tamanhos, acessibilidade, animações avançadas
 * ===========================================================================
 */

import clsx from "clsx";

interface LoaderProps {
    size?: "xs" | "sm" | "md" | "lg" | "xl";
    variant?: "primary" | "secondary" | "danger" | "neutral";
    label?: string;
    className?: string;
    inline?: boolean;
}

const sizeMap: Record<string, string> = {
    xs: "h-3 w-3 border-2",
    sm: "h-4 w-4 border-2",
    md: "h-6 w-6 border-3",
    lg: "h-8 w-8 border-4",
    xl: "h-12 w-12 border-4",
};

const variantMap: Record<string, string> = {
    primary: "border-indigo-600 border-t-transparent",
    secondary: "border-gray-500 border-t-transparent",
    danger: "border-red-600 border-t-transparent",
    neutral: "border-gray-400 border-t-transparent",
};

export default function Loader({
    size = "md",
    variant = "primary",
    label,
    inline = false,
    className,
}: LoaderProps) {
    const spinner = (
        <span
            role="status"
            aria-label={label || "Carregando"}
            className={clsx(
                "animate-spin rounded-full",
                sizeMap[size],
                variantMap[variant],
                className
            )}
        />
    );

    if (inline) return spinner;

    return (
        <div className="flex flex-col items-center justify-center gap-2 py-8">
            {spinner}
            {label && <p className="text-sm text-gray-600">{label}</p>}
        </div>
    );
}