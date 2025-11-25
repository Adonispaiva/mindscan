// Caminho completo: D:\mindscan\frontend\src\components\ui\Footer.tsx

/**
 * ===========================================================================
 *  MindScan — UI | Footer Component (Enterprise Final)
 *  Arquitetura: React 18 + TS + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Nível: Estado da Arte — Enterprise
 *  Recursos: responsividade, slots, semântica ARIA, versão institucional
 * ===========================================================================
 */

import { ReactNode } from "react";
import clsx from "clsx";

interface FooterProps {
    children?: ReactNode;
    className?: string;
    leftSlot?: ReactNode;
    rightSlot?: ReactNode;
}

export default function Footer({ children, className, leftSlot, rightSlot }: FooterProps) {
    return (
        <footer
            className={clsx(
                "w-full border-t border-gray-200 bg-white py-4 px-6 flex items-center justify-between text-sm text-gray-600",
                className
            )}
            role="contentinfo"
        >
            {/* Left Section */}
            <div className="flex items-center gap-2">
                {leftSlot}
                {children && <span>{children}</span>}
            </div>

            {/* Right Section */}
            <div className="flex items-center gap-3">
                {rightSlot}
            </div>
        </footer>
    );
}
