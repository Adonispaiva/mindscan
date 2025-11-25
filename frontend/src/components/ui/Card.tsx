// Caminho completo: D:\mindscan\frontend\src\components\ui\Card.tsx

/**
 * ===========================================================================
 *  MindScan — UI | Card Component (Enterprise Final)
 *  Arquitetura: React 18 + TS + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Nível: Estado da Arte — Enterprise
 *  Recursos: Header, Footer, Sections, Actions, Variantes, Acessibilidade
 * ===========================================================================
 */

import { ReactNode } from "react";
import clsx from "clsx";

interface CardProps {
    children: ReactNode;
    className?: string;
    shadow?: "none" | "sm" | "md" | "lg";
    padded?: boolean;
    role?: string;
}

export default function Card({
    children,
    className,
    shadow = "sm",
    padded = true,
    role = "region",
}: CardProps) {
    const shadowMap: Record<string, string> = {
        none: "",
        sm: "shadow-sm",
        md: "shadow-md",
        lg: "shadow-lg",
    };

    return (
        <section
            role={role}
            className={clsx(
                "bg-white border border-gray-200 rounded-xl",
                shadowMap[shadow],
                padded && "p-6",
                className
            )}
        >
            {children}
        </section>
    );
}

// Subcomponents --------------------------------------------------------------

interface CardHeaderProps {
    title?: string;
    subtitle?: string;
    children?: ReactNode;
}

export function CardHeader({ title, subtitle, children }: CardHeaderProps) {
    return (
        <header className="mb-4 flex flex-col gap-1">
            {title && (
                <h3 className="text-lg font-semibold tracking-tight text-gray-900">
                    {title}
                </h3>
            )}
            {subtitle && (
                <p className="text-sm text-gray-500">{subtitle}</p>
            )}
            {children}
        </header>
    );
}

interface CardSectionProps {
    children: ReactNode;
    className?: string;
}

export function CardSection({ children, className }: CardSectionProps) {
    return <div className={clsx("py-2", className)}>{children}</div>;
}

interface CardFooterProps {
    children: ReactNode;
    className?: string;
}

export function CardFooter({ children, className }: CardFooterProps) {
    return (
        <footer
            className={clsx(
                "mt-6 pt-4 border-t border-gray-200 flex justify-end gap-3",
                className
            )}
        >
            {children}
        </footer>
    );
}