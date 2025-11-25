// Caminho completo: D:\mindscan\frontend\src\components\ui\Input.tsx

/**
 * ===========================================================================
 *  MindScan — UI | Input Component (Enterprise Final)
 *  Arquitetura: React 18 + TS + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Nível: Estado da Arte — Enterprise
 *  Recursos: Acessibilidade, ícones, estados, validação, descrição, erro
 * ===========================================================================
 */

import {
    InputHTMLAttributes,
    ReactNode,
    useState,
    useId,
    FocusEvent,
} from "react";
import clsx from "clsx";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
    label?: string;
    description?: string;
    error?: string;
    leftIcon?: ReactNode;
    rightIcon?: ReactNode;
    onValidate?: (value: string) => string | null;
}

export default function Input({
    label,
    description,
    error,
    leftIcon,
    rightIcon,
    onValidate,
    className,
    onBlur,
    ...props
}: InputProps) {
    const [internalError, setInternalError] = useState<string | null>(null);
    const id = useId();

    function handleBlur(e: FocusEvent<HTMLInputElement>) {
        if (onValidate) {
            const validation = onValidate(e.target.value);
            setInternalError(validation);
        }
        onBlur?.(e);
    }

    const finalError = error || internalError;

    return (
        <div className="flex flex-col gap-1 w-full">
            {/* Label */}
            {label && (
                <label
                    htmlFor={id}
                    className="text-sm font-medium text-gray-700"
                >
                    {label}
                </label>
            )}

            {/* Input wrapper */}
            <div
                className={clsx(
                    "flex items-center gap-2 border rounded-lg px-3 py-2 transition-all bg-white",
                    finalError
                        ? "border-red-500 focus-within:ring-red-500"
                        : "border-gray-300 focus-within:ring-indigo-500 focus-within:border-indigo-500",
                    className
                )}
            >
                {/* Left Icon */}
                {leftIcon && (
                    <span className="text-gray-500 flex items-center">
                        {leftIcon}
                    </span>
                )}

                {/* Input field */}
                <input
                    id={id}
                    className="w-full outline-none bg-transparent text-gray-900 placeholder-gray-400"
                    onBlur={handleBlur}
                    {...props}
                />

                {/* Right Icon */}
                {rightIcon && (
                    <span className="text-gray-500 flex items-center">
                        {rightIcon}
                    </span>
                )}
            </div>

            {/* Description */}
            {description && !finalError && (
                <p className="text-xs text-gray-500">{description}</p>
            )}

            {/* Error */}
            {finalError && (
                <p className="text-xs text-red-600 font-medium">{finalError}</p>
            )}
        </div>
    );
}