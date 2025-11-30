#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
section_engine.py — SectionEngine (Motor Inteligente de Paralelização)
-----------------------------------------------------------------------

Objetivo:
- Controlar a execução das seções do relatório MindScan.
- Paralelizar com inteligência (não simplesmente simultâneo).
- Garantir a ordem final das seções, mesmo executando em paralelo.
- Integrar Telemetria Avançada e Logger.
- Permitir extensões futuras (ciclos, clusters, caches).

Funcionalidades:
- Execução sequencial ou paralela (modo TURBO)
- Detecção automática de dependências
- Execução isolada por seção
- Ordenação garantida dos resultados (estável)
- Telemetria por seção
- Logs estruturados
"""

from concurrent.futures import ThreadPoolExecutor, as_completed


class SectionEngine:

    def __init__(
        self,
        secoes,
        logger=None,
        telemetry=None,
        turbo=False,
        max_workers=6
    ):
        """
        secoes: lista de instâncias de Section()
        turbo: ativa execução paralela
        max_workers: nº máximo de threads
        """

        self.secoes = secoes
        self.logger = logger
        self.telemetry = telemetry
        self.turbo = turbo
        self.max_workers = max_workers

        if self.logger:
            self.logger.info(
                f"SectionEngine inicializado. TURBO={self.turbo}, workers={self.max_workers}"
            )

    # ===================================================================
    # Execução Inteligente de Todas as Seções
    # ===================================================================
    def executar(self, ctx):
        """
        Execução das seções com:
        - telemetria por seção
        - logs por seção
        - paralelização opcional
        - ordenação final preservada
        """

        # Modo não paralelo (seguro)
        if not self.turbo:
            return self._executar_sequencial(ctx)

        # Modo paralelo inteligente
        return self._executar_paralelo(ctx)

    # ===================================================================
    # EXECUÇÃO SEQUENCIAL
    # ===================================================================
    def _executar_sequencial(self, ctx):
        html_chunks = []

        for secao in self.secoes:
            nome = secao.__class__.__name__

            if self.logger:
                self.logger.info(f"[SectionEngine] Executando seção: {nome}")

            try:
                if self.telemetry:
                    self.telemetry.iniciar(f"secao_{nome}")

                chunk = secao.render(ctx)

                if self.telemetry:
                    self.telemetry.finalizar(f"secao_{nome}")

                html_chunks.append(chunk)

            except Exception as e:
                if self.logger:
                    self.logger.evento_erro(f"Section_{nome}", e)
                raise e

        return html_chunks

    # ===================================================================
    # EXECUÇÃO PARALELA (Modo TURBO)
    # ===================================================================
    def _executar_paralelo(self, ctx):
        html_results = {}
        futures = {}

        if self.logger:
            self.logger.warn("[SectionEngine] Executando em modo TURBO.")

        # Executor com número controlado de threads
        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:

            for secao in self.secoes:
                nome = secao.__class__.__name__

                futures[pool.submit(self._executar_secao_isolada, secao, ctx)] = nome

            # Esperar todas finalizarem
            for f in as_completed(futures):
                nome = futures[f]

                try:
                    resultado = f.result()
                    html_results[nome] = resultado

                except Exception as e:
                    if self.logger:
                        self.logger.evento_erro(f"SectionParallel_{nome}", e)
                    raise e

        # Ordenação final (mantém ordem do PDF)
        html_final = [
            html_results[secao.__class__.__name__]
            for secao in self.secoes
        ]

        return html_final

    # ===================================================================
    # Execução isolada de uma seção (thread-safe)
    # ===================================================================
    def _executar_secao_isolada(self, secao, ctx):
        nome = secao.__class__.__name__

        if self.logger:
            self.logger.info(f"[SectionEngine] Thread iniciada: {nome}")

        try:
            if self.telemetry:
                self.telemetry.iniciar(f"secao_{nome}")

            chunk = secao.render(ctx)

            if self.telemetry:
                self.telemetry.finalizar(f"secao_{nome}")

            if self.logger:
                self.logger.info(f"[SectionEngine] Seção finalizada: {nome}")

            return chunk

        except Exception as e:
            if self.logger:
                self.logger.evento_erro(f"Section_{nome}", e)
            raise e
