#!/usr/bin/env python3
# encoding: utf-8
"""
grade.py: script de autoevaluación del Lab 0.

Ejecuta todas las comprobaciones (tests, complejidad ciclomática, análisis estático,
cobertura) y muestra un resumen. Los mismos criterios se usan en la corrección.

Uso (desde el directorio del lab, con dependencias instaladas):
  python3 grade.py

Requisitos: pip install -r requirements.txt
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

# Umbrales (deben coincidir con test_metrics.py y pyproject.toml)
MAX_COMPLEXITY = 8
COVERAGE_MIN = 65

DIR = Path(__file__).resolve().parent
HGET_PY = DIR / "hget.py"


def run(cmd: list[str], capture: bool = True) -> tuple[int, str]:
    """Ejecuta comando; devuelve (returncode, salida)."""
    out = subprocess.run(
        cmd,
        capture_output=capture,
        text=True,
        cwd=DIR,
        timeout=120,
    )
    return (out.returncode, (out.stdout or "") + (out.stderr or ""))


def check_tests_and_coverage() -> tuple[bool, str, float | None]:
    """Ejecuta pytest con cobertura. Devuelve (ok, mensaje, porcentaje)."""
    code, out = run(
        [
            sys.executable,
            "-m",
            "pytest",
            "hget-test.py",
            "test_metrics.py",
            "-q",
            "--tb=no",
            f"--cov=hget",
            "--cov-report=term-missing",
            f"--cov-fail-under={COVERAGE_MIN}",
        ],
        capture=True,
    )
    # Buscar línea "TOTAL ... XX%"
    pct = None
    for line in out.splitlines():
        if line.strip().startswith("TOTAL"):
            m = re.search(r"(\d+)%", line)
            if m:
                pct = float(m.group(1))
            break
    ok = code == 0
    if ok:
        msg = f"Todos los tests pasan. Cobertura: {pct}% (mínimo {COVERAGE_MIN}%)."
    else:
        msg = "Algunos tests fallan o la cobertura no alcanza el mínimo."
        if pct is not None:
            msg += f" Cobertura actual: {pct}%."
    return (ok, msg, pct)


def check_complexity() -> tuple[bool, str]:
    """Comprueba complejidad ciclomática en hget.py."""
    if not HGET_PY.exists():
        return (False, f"No se encuentra {HGET_PY.name}.")
    try:
        from radon.complexity import cc_visit
    except ImportError:
        return (False, "Falta instalar radon: pip install -r requirements.txt")
    code = HGET_PY.read_text(encoding="utf-8")
    blocks = cc_visit(code)
    over = [(b.name, b.complexity) for b in blocks if b.complexity > MAX_COMPLEXITY]
    if not over:
        return (True, f"Ninguna función supera complejidad {MAX_COMPLEXITY}.")
    detalle = ", ".join(f"{n}({c})" for n, c in over[:5])
    if len(over) > 5:
        detalle += f" ... y {len(over) - 5} más"
    return (False, f"Complejidad máxima permitida: {MAX_COMPLEXITY}. Superada en: {detalle}")


def check_ruff() -> tuple[bool, str]:
    """Ejecuta ruff check en hget.py."""
    if not HGET_PY.exists():
        return (False, f"No se encuentra {HGET_PY.name}.")
    code, out = run(
        [sys.executable, "-m", "ruff", "check", str(HGET_PY), "--output-format=concise"],
        capture=True,
    )
    if code == 0:
        return (True, "Ruff: sin errores ni advertencias en hget.py.")
    lines = [l for l in out.splitlines() if l.strip() and "Found" not in l]
    preview = "\n  ".join(lines[:8]) if lines else out.strip()
    return (False, f"Ruff reporta incidencias:\n  {preview}")


def main() -> int:
    print("=" * 60)
    print("  Lab 0 — Autoevaluación (grade.py)")
    print("=" * 60)
    print()

    results: list[tuple[str, bool, str]] = []

    # 1. Tests y cobertura
    print("1. Tests y cobertura ... ", end="", flush=True)
    ok, msg, pct = check_tests_and_coverage()
    results.append(("Tests y cobertura", ok, msg))
    print("OK" if ok else "FALLO")
    if not ok and "Cobertura actual" in msg:
        print("   ", msg.split(" Cobertura actual")[0])
        print("   Cobertura actual:", f"{pct}%" if pct is not None else "—")
    else:
        print("   ", msg)
    print()

    # 2. Complejidad ciclomática
    print("2. Complejidad ciclomática ... ", end="", flush=True)
    ok, msg = check_complexity()
    results.append(("Complejidad ciclomática", ok, msg))
    print("OK" if ok else "FALLO")
    print("   ", msg)
    print()

    # 3. Análisis estático (ruff)
    print("3. Análisis estático (ruff) ... ", end="", flush=True)
    ok, msg = check_ruff()
    results.append(("Ruff", ok, msg))
    print("OK" if ok else "FALLO")
    if not ok and "\n" in msg:
        for line in msg.split("\n")[1:]:
            print("  ", line)
    else:
        print("   ", msg)
    print()

    # Resumen final
    all_ok = all(r[1] for r in results)
    print("=" * 60)
    if all_ok:
        print("  RESULTADO: CUMPLE todas las condiciones de aprobación")
    else:
        print("  RESULTADO: NO CUMPLE alguna condición de aprobación")
        failed = [r[0] for r in results if not r[1]]
        print("  Revisar:", ", ".join(failed))
    print("=" * 60)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
