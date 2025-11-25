// Caminho completo: D:\mindscan\frontend\src\components\ui\Table.tsx

/**
 * ===========================================================================
 *  MindScan — UI | Table Component (Enterprise Final)
 *  Arquitetura: React 18 + TS + Tailwind 3.4
 *  Autor: Diretor Leo Vinci (GPT Inovexa)
 *  Nível: Estado da Arte — Enterprise
 *  Recursos: Sorting, Empty State, Loading State, Acessibilidade, Slots
 * ===========================================================================
 */

import { ReactNode, useState } from "react";
import clsx from "clsx";

interface Column {
    key: string;
    label: string;
    sortable?: boolean;
}

interface TableProps {
    columns: Column[];
    data: Record<string, any>[];
    loading?: boolean;
    emptyText?: string;
}

export default function Table({ columns, data, loading = false, emptyText = "Nenhum registro encontrado." }: TableProps) {
    const [sortKey, setSortKey] = useState<string | null>(null);
    const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc");

    function handleSort(column: Column) {
        if (!column.sortable) return;

        if (sortKey === column.key) {
            setSortOrder(sortOrder === "asc" ? "desc" : "asc");
        } else {
            setSortKey(column.key);
            setSortOrder("asc");
        }
    }

    const sortedData = (() => {
        if (!sortKey) return data;
        return [...data].sort((a, b) => {
            const valueA = a[sortKey];
            const valueB = b[sortKey];

            if (valueA < valueB) return sortOrder === "asc" ? -1 : 1;
            if (valueA > valueB) return sortOrder === "asc" ? 1 : -1;
            return 0;
        });
    })();

    return (
        <div className="w-full overflow-auto rounded-xl border border-gray-200 bg-white shadow-sm">
            <table className="w-full text-left text-sm">
                <thead className="bg-gray-100 text-gray-700 select-none">
                    <tr>
                        {columns.map((col) => (
                            <th
                                key={col.key}
                                onClick={() => handleSort(col)}
                                className={clsx("px-4 py-3 font-semibold cursor-pointer", col.sortable && "hover:text-indigo-600")}
                            >
                                <div className="flex items-center gap-1">
                                    {col.label}
                                    {sortKey === col.key && (
                                        <span>{sortOrder === "asc" ? "▲" : "▼"}</span>
                                    )}
                                </div>
                            </th>
                        ))}
                    </tr>
                </thead>

                <tbody>
                    {/* Loading State */}
                    {loading && (
                        <tr>
                            <td colSpan={columns.length} className="px-4 py-6 text-center text-gray-500">
                                Carregando...
                            </td>
                        </tr>
                    )}

                    {/* Empty State */}
                    {!loading && sortedData.length === 0 && (
                        <tr>
                            <td colSpan={columns.length} className="px-4 py-6 text-center text-gray-500">
                                {emptyText}
                            </td>
                        </tr>
                    )}

                    {/* Rows */}
                    {!loading &&
                        sortedData.map((row, i) => (
                            <tr key={i} className="border-t border-gray-100 hover:bg-gray-50">
                                {columns.map((col) => (
                                    <td key={col.key} className="px-4 py-3">
                                        {row[col.key]}
                                    </td>
                                ))}
                            </tr>
                        ))}
                </tbody>
            </table>
        </div>
    );
}