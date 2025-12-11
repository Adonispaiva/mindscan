# Arquivo normalizado pelo MindScan Optimizer (Final Version)
# Caminho: D:\projetos-inovexa\mindscan\backend\models\scoring\scoring_teique.py
# Última atualização: 2025-12-11T09:59:21.042587

import Link from "next/link";
import { TrendingUp, TrendingDown, ArrowRight } from "lucide-react";

interface RecommendationItemProps {
  title: string;
  trend: string;       // ex: "+12%" ou "-3%"
  reason: string;      // explicação curta
  href: string;
}

export default function RecommendationItem({
  title,
  trend,
  reason,
  href,
}: RecommendationItemProps) {

  const isPositive = trend.startsWith("+");
  const isNegative = trend.startsWith("-");

  return (
    <div className="bg-white dark:bg-gray-950 rounded-xl shadow-md border border-gray-200 dark:border-gray-800 p-6 flex flex-col gap-4 hover:shadow-xl transition">

      {/* TÍTULO E TENDÊNCIA */}
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
          {title}
        </h3>

        <span
          className={`flex items-center gap-1 px-3 py-1 rounded-full text-xs font-semibold ${
            isPositive
              ? "bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300"
              : isNegative
              ? "bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300"
              : "bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300"
          }`}
        >
          {isPositive && <TrendingUp size={14} />}
          {isNegative && <TrendingDown size={14} />}
          {trend}
        </span>
      </div>

      {/* MOTIVO / JUSTIFICATIVA */}
      <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed flex-1">
        {reason}
      </p>

      {/* AÇÃO */}
      <Link
        href={href}
        className="flex items-center gap-2 mt-auto px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition"
      >
        Ver Produto <ArrowRight size={16} />
      </Link>
    </div>
  );
}
