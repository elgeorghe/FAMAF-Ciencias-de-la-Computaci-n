#!/usr/bin/env python3
# encoding: utf-8
"""
Tests de métricas de calidad: complejidad ciclomática, análisis estático y cobertura.

Obligatorios para la entrega del lab. Los umbrales deben coincidir con grade.py y pyproject.toml:
- Complejidad ciclomática: ninguna función/método en src/ por encima del límite.
- Análisis estático (ruff): cero errores o advertencias en src/.
- Cobertura: configurada en pyproject.toml (pytest --cov-fail-under).

Uso: pytest tests/ -v   (incluye este archivo vía testpaths)
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


# Umbral máximo de complejidad ciclomática por función (McCabe).
# Exigente: ninguna función debe superar este valor. Debe coincidir con grade.py.
MAX_CYCLOMATIC_COMPLEXITY = 8

# Directorio a analizar (código del lab).
SRC = Path(__file__).resolve().parent.parent / "src"


def test_cyclomatic_complexity() -> None:
    """Ninguna función en src/ debe superar la complejidad ciclomática máxima."""
    import radon.complexity as radon_cc

    over: list[tuple[str, str, int]] = []
    for py_file in sorted(SRC.rglob("*.py")):
        code = py_file.read_text(encoding="utf-8")
        blocks = radon_cc.cc_visit(code)
        rel_path = py_file.relative_to(SRC)
        for b in blocks:
            if b.complexity > MAX_CYCLOMATIC_COMPLEXITY:
                over.append((str(rel_path), b.name, b.complexity))
    assert not over, (
        f"Complejidad ciclomática máxima permitida: {MAX_CYCLOMATIC_COMPLEXITY}. "
        f"Superada en: {over}"
    )


def test_static_analysis_ruff() -> None:
    """Ruff no debe reportar errores ni advertencias en src/."""
    result = subprocess.run(
        [sys.executable, "-m", "ruff", "check", str(SRC), "--output-format=concise"],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=Path(__file__).resolve().parent.parent,
    )
    assert result.returncode == 0, (
        f"Análisis estático (ruff) falló en src/:\n"
        f"{result.stdout or result.stderr}"
    )


def test_coverage_enforced_by_pytest_cov() -> None:
    """
    La cobertura mínima se exige vía pytest-cov (--cov-fail-under en pyproject.toml).
    Este test solo documenta que la suite debe ejecutarse con pytest (no solo unittest).
    """
    assert True, "Cobertura: ejecutar pytest (con pytest-cov) para comprobar el umbral."
