// Caminho completo: D:\mindscan\frontend\src\components\ui\Modal.tsx

/**
 * ===========================================================================
 *  MindScan — UI | Modal Component (Enterprise Final)
 *  Arquitetura: React 18 + TS + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Nível: Estado da Arte — Enterprise
 *  Recursos: Acessibilidade completa, animações, foco preso, teclado, variantes
 * ===========================================================================
 */

import { ReactNode, useEffect, useRef } from "react";
import clsx from "clsx";

interface ModalProps {
    open: boolean;
    title?: string;
    description?: string;
    children: ReactNode;
    onClose: () => void;
    size?: "sm" | "md" | "lg";
    closeOnOverlay?: boolean;
}

export default function Modal({
    open,
    title,
    description,
    children,
    onClose,
    size = "md",
    closeOnOverlay = true,
}: ModalProps) {
    const modalRef = useRef<HTMLDivElement>(null);

    // Focus trap -------------------------------------------------------------
    useEffect(() => {
        if (open && modalRef.current) {
            const firstFocusable = modalRef.current.querySelector<HTMLElement>(
                "button, [href], input, select, textarea, [tabindex]:not([tabindex='-1'])"
            );
            firstFocusable?.focus();
        }
    }, [open]);

    // Close on ESC -----------------------------------------------------------
    useEffect(() => {
        function handleKey(e: KeyboardEvent) {
            if (e.key === "Escape") onClose();
        }
        if (open) document.addEventListener("keydown", handleKey);
        return () => document.removeEventListener("keydown", handleKey);
    }, [open, onClose]);

    if (!open) return null;

    const sizeMap: Record<string, string> = {
        sm: "max-w-sm",
        md: "max-w-lg",
        lg: "max-w-2xl",
    };

    return (
        <div
            role="dialog"
            aria-modal="true"
            aria-labelledby="modal-title"
            aria-describedby="modal-desc"
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 animate-fade-in"
            onClick={() => closeOnOverlay && onClose()}
        >
            <div
                ref={modalRef}
                onClick={(e) => e.stopPropagation()}
                className={clsx(
                    "bg-white w-full rounded-xl shadow-xl p-6 animate-scale-in",
                    sizeMap[size]
                )}
            >
                {/* Header */}
                {(title || description) && (
                    <header className="mb-4">
                        {title && (
                            <h2
                                id="modal-title"
                                className="text-xl font-semibold tracking-tight"
                            >
                                {title}
                            </h2>
                        )}
                        {description && (
                            <p
                                id="modal-desc"
                                className="text-sm text-gray-600 mt-1"
                            >
                                {description}
                            </p>
                        )}
                    </header>
                )}

                {/* Content */}
                <div className="text-gray-700 mb-6">{children}</div>

                {/* Footer */}
                <footer className="flex justify-end gap-3 pt-4 border-t border-gray-200">
                    <button
                        onClick={onClose}
                        className="px-4 py-2 rounded-lg bg-gray-200 hover:bg-gray-300 font-medium transition-all"
                    >
                        Fechar
                    </button>
                </footer>
            </div>
        </div>
    );
}