#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setup.py — Compatibilidade clássica para instalação do pacote MindScan PDF Engine.

Este arquivo permite:
    python setup.py install
    python setup.py sdist bdist_wheel
    pip install .

Mesmo com o pyproject.toml sendo o arquivo principal, o setup.py garante
compatibilidade com ambientes mais antigos ou ferramentas de build.
"""

from setuptools import setup

if __name__ == "__main__":
    setup()
