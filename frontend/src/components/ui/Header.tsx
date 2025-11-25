/**
 * ===========================================================================
 *  MindScan — UI | Header Component (Enterprise Final)
 *  Arquitetura: React 18 + TS + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Nível: Estado da Arte — Enterprise
 *  Recursos: slots, breadcrumbs, actions, responsividade, ARIA
 * ===========================================================================
 */

import { ReactNode } from "react";
import clsx from "clsx";

interface HeaderProps {
    title: string;
    subtitle?: string;
    breadcrumbs?: ReactNode;
    actions?: ReactNode;
    className?: string;
}

export default function Header({
    title,
    subtitle,
    breadcrumbs,
    actions,
    className,
}: HeaderProps) {
    return (
        <header
            className={clsx(
                "w-full flex flex-col gap-3 py-4 border-b border-gray-200 bg-white",
                className
            )}
            role="banner"
        >
            {/* Breadcrumbs */}
            {breadcrumbs && (
                <nav aria-label="Breadcrumb" className="text-sm text-gray-500">
                    {breadcrumbs}
                </nav>
            )}

            {/* Title + Actions */}
            <div className="flex items-center justify-between gap-6">
                <div className="flex flex-col">
                    <h1 className="text-2xl font-semibold tracking-tight text-gray-900">
                        {title}
                    </h1>
                    {subtitle && (
                        <p className="text-gray-600 text-sm mt-1">{subtitle}</p>
                    )}
                </div>

                {actions && (
                    <div className="flex items-center gap-3">{actions}</div>
                )}
            </div>
        </header>
    );
}
