DB_PATH ?= instance/datos.db

.PHONY: run test grade lint docker-build docker-run docker-test docker-grade clean-db help

PYTHON ?= python3
VENV = .venv
BIN = $(VENV)/bin

help:
	@echo "Targets: run, test, grade, lint, docker-build, docker-run, docker-test, docker-grade, clean-db"

run:
	$(PYTHON) -m src.app

test:
	PYTHONPATH=. $(PYTHON) -m pytest tests/ -v --tb=short

grade:
	PYTHONPATH=. $(PYTHON) grade.py

lint:
	$(PYTHON) -m ruff check src/
	$(PYTHON) -m radon cc src -s -a

docker-build:
	docker build -t lab1-2026-api .

docker-run:
	docker run --rm -p 5000:5000 --env-file .env lab1-2026-api

# Ejecuta los tests (pytest) dentro de un contenedor Docker (sin grading completo).
docker-test:
	docker run --rm -v "$(CURDIR)":/app -w /app -e PYTHONPATH=/app python:3.10-slim bash -c "pip install -q --no-cache-dir -r requirements.txt && python -m pytest tests/ -v --tb=short"

# Ejecuta make grade dentro de un contenedor (monta el directorio actual; no requiere venv local).
docker-grade:
	docker run --rm -v "$(CURDIR)":/app -w /app -e PYTHONPATH=/app python:3.10-slim bash -c "pip install -q --no-cache-dir -r requirements.txt && python grade.py"

# Borra la base SQLite para empezar de cero con datos vacíos (path por defecto: instance/datos.db).
clean-db:
	@rm -f $(DB_PATH)
	@echo "Base de datos eliminada (si existía)."
