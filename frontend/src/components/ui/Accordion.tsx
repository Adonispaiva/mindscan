// Caminho completo: D:\mindscan\frontend\src\components\ui\Accordion.tsx

/**
 * ===========================================================================
 *  MindScan — UI | Accordion Component (Enterprise Final)
 *  Arquitetura: React 18 + TS + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Nível: Estado da Arte — Enterprise
 *  Recursos: múltiplas seções, ARIA, teclado, animação, collapse suave
 * ===========================================================================
 */

import { ReactNode, useState } from "react";
import clsx from "clsx";

interface AccordionItem {
    title: string;
    content: ReactNode;
    disabled?: boolean;
}

interface AccordionProps {
    items: AccordionItem[];
    allowMultiple?: boolean;
    defaultOpen?: number[];
    className?: string;
}

export default function Accordion({
    items,
    allowMultiple = false,
    defaultOpen = [],
    className,
}: AccordionProps) {
    const [openIndexes, setOpenIndexes] = useState<number[]>(defaultOpen);

    function toggle(index: number) {
        if (items[index].disabled) return;

        if (allowMultiple) {
            setOpenIndexes((prev) =>
                prev.includes(index)
                    ? prev.filter((i) => i !== index)
                    : [...prev, index]
            );
        } else {
            setOpenIndexes((prev) =>
                prev.includes(index) ? [] : [index]
            );
        }
    }

    return (
        <div className={clsx("flex flex-col divide-y divide-gray-200", className)}>
            {items.map((item, i) => {
                const isOpen = openIndexes.includes(i);
                return (
                    <div key={i}>
                        <button
                            role="button"
                            aria-expanded={isOpen}
                            disabled={item.disabled}
                            onClick={() => toggle(i)}
                            className={clsx(
                                "w-full flex justify-between items-center py-4 px-2 text-left font-medium transition-all",
                                item.disabled
                                    ? "text-gray-400 cursor-not-allowed"
                                    : "text-gray-900 hover:bg-gray-50"
                            )}
                        >
                            {item.title}
                            <span className="text-xl">
                                {isOpen ? "−" : "+"}
                            </span>
                        </button>

                        {/* Conteúdo */}
                        <div
                            className={clsx(
                                "overflow-hidden transition-all", 
                                isOpen ? "max-h-screen py-2" : "max-h-0"
                            )}
                        >
                            <div className="text-gray-700 text-sm px-2 pb-2">
                                {item.content}
                            </div>
                        </div>
                    </div>
                );
            })}
        </div>
    );
}
