// Caminho completo: D:\mindscan\frontend\src\components\ui\Breadcrumbs.tsx

/**
 * ===========================================================================
 *  MindScan — UI | Breadcrumbs Component (Enterprise Final)
 *  Arquitetura: React 18 + TS + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Nível: Estado da Arte — Enterprise
 *  Recursos: navegação hierárquica, ARIA, responsividade, separators dinâmicos
 * ===========================================================================
 */

import { ReactNode } from "react";
import { NavLink } from "react-router-dom";
import clsx from "clsx";

interface Crumb {
    label: string;
    to?: string;
}

interface BreadcrumbsProps {
    items: Crumb[];
    separator?: ReactNode;
    className?: string;
}

export default function Breadcrumbs({ items, separator = "/", className }: BreadcrumbsProps) {
    return (
        <nav
            aria-label="Breadcrumb"
            className={clsx("flex items-center gap-2 text-sm text-gray-500", className)}
        >
            {items.map((item, index) => (
                <div key={index} className="flex items-center gap-2">
                    {item.to ? (
                        <NavLink
                            to={item.to}
                            className="hover:text-indigo-600 transition-colors"
                        >
                            {item.label}
                        </NavLink>
                    ) : (
                        <span className="font-medium text-gray-700">{item.label}</span>
                    )}

                    {index < items.length - 1 && (
                        <span className="select-none text-gray-400">{separator}</span>
                    )}
                </div>
            ))}
        </nav>
    );
}
