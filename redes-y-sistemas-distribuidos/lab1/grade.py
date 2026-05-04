#!/usr/bin/env python3
"""
Script de grading: ejecuta pytest (test_public + test_private + test_metrics + tests
de integración), coverage, ruff, complejidad ciclomática y algunos chequeos
adicionales de autenticación y uso de git.

Umbrales bloqueantes:
- Cobertura >= MIN_COVERAGE sobre src/.
- Sin errores de ruff en src/.
- Ninguna función por encima de MAX_COMPLEXITY.
- Autenticación básica implementada (hash de contraseña y expiración de tokens).

Los chequeos de git producen **warnings no bloqueantes** que ayudan a evaluar
la dimensión "Git y buenas prácticas" de la rúbrica.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
TESTS = ROOT / "tests"
MIN_COVERAGE = 70
MAX_COMPLEXITY = 8


def run(
    cmd: list[str],
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    env_final: dict[str, str] = env or os.environ.copy()
    return subprocess.run(
        cmd,
        cwd=cwd or ROOT,
        env=env_final,
        capture_output=True,
        text=True,
        timeout=120,
    )


def check_complexity() -> tuple[bool, str]:
    """Comprueba que ninguna función en src/ supere MAX_COMPLEXITY."""
    try:
        from radon.complexity import cc_visit
    except ImportError:
        return (False, "Falta instalar radon: pip install -r requirements.txt")
    over: list[tuple[str, str, int]] = []
    for py_file in sorted(SRC.rglob("*.py")):
        code = py_file.read_text(encoding="utf-8")
        blocks = cc_visit(code)
        rel_path = py_file.relative_to(SRC)
        for b in blocks:
            if b.complexity > MAX_COMPLEXITY:
                over.append((str(rel_path), b.name, b.complexity))
    if not over:
        return (True, f"Ninguna función supera complejidad {MAX_COMPLEXITY}.")
    detalle = ", ".join(f"{p}:{n}({c})" for p, n, c in over[:5])
    if len(over) > 5:
        detalle += f" ... y {len(over) - 5} más"
    return (False, f"Complejidad máxima permitida: {MAX_COMPLEXITY}. Superada en: {detalle}")


def _git_available() -> bool:
    """Devuelve True si git está disponible en el entorno."""
    try:
        r = run(["git", "--version"])
    except OSError:
        return False
    return r.returncode == 0


def _git_warnings() -> list[str]:
    """Calcula warnings no bloqueantes sobre el uso de git."""
    if not _git_available():
        return ["git no está disponible en el entorno; no se evaluará uso de git desde grade.py."]

    warnings: list[str] = []

    # 1) Cantidad total de commits
    r = run(["git", "rev-list", "--count", "HEAD"])
    try:
        total_commits = int((r.stdout or "0").strip() or "0")
    except ValueError:
        total_commits = 0
    if total_commits < 5:
        warnings.append(
            f"muy pocos commits en el repositorio ({total_commits}); revisar buenas prácticas de git."
        )

    # 2) Mensajes de commit poco descriptivos
    r = run(["git", "log", "--pretty=%s", "-n", "20"])
    subjects = [s.strip() for s in (r.stdout or "").splitlines() if s.strip()]
    if subjects:
        unique_subjects = set(subjects)
        if len(unique_subjects) == 1:
            only = next(iter(unique_subjects))
            warnings.append(
                f"todos los commits recientes tienen el mismo mensaje ('{only}'); mensajes poco descriptivos."
            )

    # 3) Distribución por autor (participación)
    try:
        r = run(["git", "shortlog", "-s", "-n"])
    except Exception:
        # Si algo raro pasa (repositorio muy grande, tiempo excedido, etc.),
        # devolvemos un warning genérico y no bloqueamos el grade.
        warnings.append("no se pudo obtener git shortlog; revisar participación manualmente.")
        return warnings

    lines = [ln.strip() for ln in (r.stdout or "").splitlines() if ln.strip()]
    authors: list[tuple[int, str]] = []
    for ln in lines:
        parts = ln.split("\t", maxsplit=1)
        if len(parts) != 2:
            continue
        try:
            count = int(parts[0].strip())
        except ValueError:
            continue
        name = parts[1].strip()
        authors.append((count, name))
    if len(authors) >= 2:
        total = sum(c for c, _ in authors)
        top_count, top_name = authors[0]
        if total > 0 and top_count / total > 0.8:
            warnings.append(
                f"un único autor concentra la mayoría de los commits ({top_name}: {top_count}/{total}); revisar reparto de trabajo."
            )

    return warnings


def _auth_security_checks() -> list[str]:
    """Checks bloqueantes sobre autenticación básica (hash y expiración de tokens)."""
    issues: list[str] = []

    auth_py = SRC / "auth.py"
    if not auth_py.exists():
        # Debería estar siempre; si no, los tests públicos fallarán.
        return []

    content = auth_py.read_text(encoding="utf-8")

    # Uso de hashing seguro
    if "generate_password_hash" not in content or "check_password_hash" not in content:
        issues.append(
            "auth.py no usa generate_password_hash/check_password_hash; revisar Parte 6 (hash de contraseña)."
        )

    # Presencia de patrones claramente inseguros
    if "password_hash = password" in content:
        issues.append(
            "se encontró 'password_hash = password' en auth.py; no se deben guardar contraseñas en texto plano."
        )

    # Token y expiración
    if "token_expira_en" not in content:
        issues.append(
            "auth.py no maneja el campo token_expira_en; implementar expiración de tokens (Parte 6)."
        )

    # Check mínimo de obtención de usuario actual
    if "def obtener_usuario_actual" not in content:
        issues.append(
            "auth.py no define obtener_usuario_actual; la autorización por token no puede funcionar correctamente."
        )

    return issues


def _logging_checks() -> list[str]:
    """Checks bloqueantes sobre logging mínimo por request y presencia de README."""
    issues: list[str] = []

    # Logging mínimo: verificar que app.py registre método, path y código de respuesta.
    app_py = SRC / "app.py"
    if app_py.exists():
        content = app_py.read_text(encoding="utf-8")
        # Requisito mínimo: una llamada a logger.info que incluya method, path y status_code.
        if "logger.info" not in content or "request.method" not in content or "request.path" not in content or "response.status_code" not in content:
            issues.append(
                "logging mínimo no detectado en app.py: se espera un log por request con método, path y código de respuesta (ver hooks before_request/after_request)."
            )
    else:
        # Si no existe app.py, los tests probablemente ya fallen; no agregamos issue extra.
        pass

    # README y link al video.
    readme = ROOT / "README.md"
    if not readme.exists():
        issues.append("README.md no encontrado en la raíz del proyecto.")
    else:
        readme_content = readme.read_text(encoding="utf-8")
        if "http://" not in readme_content and "https://" not in readme_content:
            issues.append(
                "README.md no contiene ningún enlace (se espera al menos el link al video de presentación)."
            )

    return issues


def main() -> int:
    print("=== Grading API Recomendador de Videojuegos ===\n")
    exit_code = 0

    # 1. Pytest con cobertura (test_public, test_private, test_metrics, integración)
    print("1. Tests (pytest + coverage)...")
    r = run(
        [
            sys.executable,
            "-m",
            "pytest",
            str(TESTS),
            "-v",
            "--tb=short",
            f"--cov={SRC.name}",
            "--cov-report=term-missing",
            f"--cov-fail-under={MIN_COVERAGE}",
        ],
        env={**os.environ, "PYTHONPATH": str(ROOT)},
    )
    if r.returncode != 0:
        print(r.stdout)
        print(r.stderr)
        print("FAIL: tests fallaron o cobertura por debajo del mínimo.\n")
        exit_code = 1
    else:
        print(r.stdout)
        print("OK: tests pasaron y cobertura suficiente.\n")

    # 2. Ruff
    print("2. Lint (ruff)...")
    r = run([sys.executable, "-m", "ruff", "check", str(SRC)])
    if r.returncode != 0:
        print(r.stdout)
        print("FAIL: ruff encontró errores o warnings.\n")
        exit_code = 1
    else:
        print("OK: ruff sin errores.\n")

    # 3. Complejidad ciclomática (radon: mostrar detalle y luego comprobar umbral)
    print("3. Complejidad (radon cc)...")
    r = run([sys.executable, "-m", "radon", "cc", str(SRC), "-s", "-a"])
    if r.stdout.strip():
        print(r.stdout)
    ok, msg = check_complexity()
    if not ok:
        print("FAIL:", msg, "\n")
        exit_code = 1
    else:
        print("OK:", msg, "\n")

    # 4. Chequeos adicionales de autenticación (hash + expiración)
    print("4. Autenticación básica (checks estáticos)...")
    auth_issues = _auth_security_checks()
    if auth_issues:
        for issue in auth_issues:
            print("FAIL:", issue)
        exit_code = 1
    else:
        print("OK: auth.py parece usar hashing y expiración de tokens.\n")

    # 5. Logging mínimo y README
    print("5. Logging mínimo y README.md...")
    log_readme_issues = _logging_checks()
    if log_readme_issues:
        for issue in log_readme_issues:
            print("FAIL:", issue)
        exit_code = 1
    else:
        print("OK: logging mínimo y README.md detectados.\n")

    # 6. Warnings sobre uso de git (no bloqueantes)
    print("6. Warnings de git (no bloqueantes)...")
    git_warns = _git_warnings()
    if not git_warns:
        print("OK: sin warnings de git detectados.\n")
    else:
        for w in git_warns:
            print("WARNING (git):", w)
        print()

    print("=== Fin grading ===")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
