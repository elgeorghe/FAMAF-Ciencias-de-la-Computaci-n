#!/usr/bin/env python3
# encoding: utf-8
"""
Tests de métricas de calidad: complejidad ciclomática, análisis estático y cobertura.

Obligatorios para la entrega del lab. Los umbrales son exigentes:
- Complejidad ciclomática: ninguna función/método por encima del límite.
- Análisis estático (ruff): cero errores o advertencias en hget.py.
- Cobertura: configurada en pyproject.toml (pytest --cov-fail-under).

Uso: pytest test_metrics.py -v   (o pytest sin args para incluir también hget-test.py)
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

# Umbral máximo de complejidad ciclomática por función (McCabe).
# Exigente: ninguna función debe superar este valor.
MAX_CYCLOMATIC_COMPLEXITY = 8

# Archivo a analizar (solución del lab).
HGET_PY = Path(__file__).resolve().parent / "hget.py"


def test_cyclomatic_complexity() -> None:
    """Ninguna función en hget.py debe superar la complejidad ciclomática máxima."""
    import radon.complexity as radon_cc

    code = HGET_PY.read_text(encoding="utf-8")
    blocks = radon_cc.cc_visit(code)
    over = [
        (b.name, b.complexity)
        for b in blocks
        if b.complexity > MAX_CYCLOMATIC_COMPLEXITY
    ]
    assert not over, (
        f"Complejidad ciclomática máxima permitida: {MAX_CYCLOMATIC_COMPLEXITY}. "
        f"Superada en: {over}"
    )


def test_static_analysis_ruff() -> None:
    """Ruff no debe reportar errores ni advertencias en hget.py."""
    result = subprocess.run(
        [sys.executable, "-m", "ruff", "check", str(HGET_PY), "--output-format=concise"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0, (
        f"Análisis estático (ruff) falló en {HGET_PY.name}:\n"
        f"{result.stdout or result.stderr}"
    )


def test_coverage_enforced_by_pytest_cov() -> None:
    """
    La cobertura mínima se exige vía pytest-cov (--cov-fail-under en pyproject.toml).
    Este test solo documenta que la suite debe ejecutarse con pytest (no solo unittest).
    """
    # Si pytest se ejecuta con pytest-cov, la cobertura se comprueba automáticamente.
    assert True, "Cobertura: ejecutar pytest (con pytest-cov) para comprobar el umbral."
