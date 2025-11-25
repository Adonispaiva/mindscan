// Caminho completo: D:\mindscan\frontend\src\components\ui\Tabs.tsx

/**
 * ===========================================================================
 *  MindScan — UI | Tabs Component (Enterprise Final)
 *  Arquitetura: React 18 + TS + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Nível: Estado da Arte — Enterprise
 *  Recursos: estados internos, ARIA, teclado, variantes, animação
 * ===========================================================================
 */

import { ReactNode, useState } from "react";
import clsx from "clsx";

interface Tab {
    label: string;
    content: ReactNode;
    disabled?: boolean;
}

interface TabsProps {
    tabs: Tab[];
    initialIndex?: number;
    variant?: "line" | "pill";
    className?: string;
}

export default function Tabs({
    tabs,
    initialIndex = 0,
    variant = "line",
    className,
}: TabsProps) {
    const [index, setIndex] = useState(initialIndex);

    const variantMap: Record<string, string> = {
        line: "border-b-2 border-transparent hover:border-gray-300",
        pill: "rounded-lg px-3 py-1 bg-gray-100 text-gray-700 hover:bg-gray-200",
    };

    return (
        <div className={clsx("flex flex-col gap-4", className)}>
            {/* Tab List */}
            <div
                role="tablist"
                className="flex items-center gap-4 border-b border-gray-200 pb-2"
            >
                {tabs.map((tab, i) => (
                    <button
                        key={i}
                        role="tab"
                        aria-selected={index === i}
                        aria-disabled={tab.disabled}
                        disabled={tab.disabled}
                        onClick={() => setIndex(i)}
                        className={clsx(
                            "text-sm font-medium transition-all pb-2",
                            !tab.disabled && variantMap[variant],
                            index === i &&
                                (variant === "line"
                                    ? "border-indigo-600 text-indigo-600"
                                    : "bg-indigo-600 text-white")
                        )}
                    >
                        {tab.label}
                    </button>
                ))}
            </div>

            {/* Tab Panel */}
            <div role="tabpanel" className="animate-fade-in">
                {tabs[index].content}
            </div>
        </div>
    );
}
