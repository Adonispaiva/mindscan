// Caminho completo: D:\mindscan\frontend\src\components\ui\Avatar.tsx

/**
 * ===========================================================================
 *  MindScan — UI | Avatar Component (Enterprise Final)
 *  Arquitetura: React 18 + TS + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Nível: Estado da Arte — Enterprise
 *  Recursos: fallback automático, inicial, tamanhos, variantes, ARIA
 * ===========================================================================
 */

import { ReactNode, useState } from "react";
import clsx from "clsx";

interface AvatarProps {
    src?: string;
    alt?: string;
    size?: "sm" | "md" | "lg" | "xl";
    rounded?: "sm" | "md" | "lg" | "full";
    fallbackIcon?: ReactNode;
    className?: string;
}

const sizeMap: Record<string, string> = {
    sm: "h-8 w-8 text-sm",
    md: "h-10 w-10 text-base",
    lg: "h-14 w-14 text-lg",
    xl: "h-20 w-20 text-xl",
};

const roundedMap: Record<string, string> = {
    sm: "rounded",
    md: "rounded-md",
    lg: "rounded-xl",
    full: "rounded-full",
};

export default function Avatar({
    src,
    alt = "Avatar do usuário",
    size = "md",
    rounded = "full",
    fallbackIcon,
    className,
}: AvatarProps) {
    const [failed, setFailed] = useState(false);

    return (
        <div
            role="img"
            aria-label={alt}
            className={clsx(
                "flex items-center justify-center bg-gray-200 text-gray-700 overflow-hidden select-none",
                sizeMap[size],
                roundedMap[rounded],
                className
            )}
        >
            {src && !failed ? (
                <img
                    src={src}
                    alt={alt}
                    className="object-cover w-full h-full"
                    onError={() => setFailed(true)}
                />
            ) : fallbackIcon ? (
                <span className="text-current">{fallbackIcon}</span>
            ) : (
                <span className="font-semibold">
                    {alt.charAt(0).toUpperCase()}
                </span>
            )}
        </div>
    );
}