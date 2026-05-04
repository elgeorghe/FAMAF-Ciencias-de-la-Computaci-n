# Recomendador de Videojuegos — Laboratorio 1 (2026)

Proyecto base para implementar la API según el contrato en `openapi.yaml`. El archivo **openapi.yaml** define los endpoints; las rutas están registradas en **app.py** y la lógica de cada una se implementa en los módulos de **src/** (usuarios, juegos, sugerencias, wikidata, filtros).

## Requisitos

- **Docker (recomendado)** para ejecutar la API y el grading sin instalar Python localmente.
- Alternativa: Python 3.10 o superior, venv y `pip install -r requirements.txt`.

## Orden sugerido de trabajo

1. **Configurar entorno y explorar el proyecto:** usá Docker (`make docker-build`, `make docker-run`) o venv y `make run`. Abrí http://localhost:5000/docs, leé el contrato de la API y probá los endpoints (aunque respondan 501). Ejecutá `make test` (o `make grade`) y leé los errores para entender qué esperan los tests. Luego implementá usuarios, lista de juegos, Wikidata y completá tests en `test_private` hasta que `make grade` pase.
2. **Usuarios:** implementar CRUD de usuarios y probar con curl.
3. **Lista de juegos:** implementar lista de juegos por usuario y filtros.
4. **Wikidata:** integrar búsqueda y mapeo desde Wikidata.
5. **Tests y calidad:** completar tests en `test_private` y asegurar que `make grade` (o `make docker-grade`) pase.

## Configuración y uso

### Con Docker (recomendado)

```bash
make docker-build
make docker-run
```

Con la API corriendo, abrí **http://localhost:5000/docs**. Para verificar tests, cobertura, lint y complejidad sin tener Python local:

```bash
make docker-grade
```

Necesitás un archivo `.env` en la raíz (copiá desde `.env.example`). Los datos se persisten en SQLite (por defecto `instance/datos.db`). Para volver a empezar con datos vacíos: `make clean-db`.

### Alternativa con venv

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # Opcional: WIKIDATA_USER_AGENT para llamadas a Wikidata
make run
```
Si no usás make: `PYTHONPATH=. python3 -m src.app`.

- `make test` — Ejecuta los tests
- `make grade` — Ejecuta el script de grading (tests + cobertura + lint + complejidad)
- `make lint` — Ruff y radon
- `make clean-db` — Borra la base SQLite para empezar de cero con datos vacíos

Los tests en **test_metrics.py** comprueban estilo (ruff) y complejidad ciclomática; si fallan, corregir el código en **src/** (refactorizar funciones demasiado largas o con muchas ramas).

## Glosario

Deben completar en el README (o en un archivo referenciado desde él) un **glosario** con definiciones de los conceptos del laboratorio. Incluir al menos: API REST, endpoint, recurso, idempotencia, contrato de API, cobertura de tests, complejidad ciclomática, linters, Docker, health check, timeout, variables de entorno, y los que se mencionan en el enunciado (por ejemplo en "Antes de empezar: conceptos de red"). Agregar además otros términos que les parezcan relevantes para el proyecto.

## Enunciado

Ver **enunciado.md** en esta carpeta para las fases del laboratorio y entregables. La **Parte 1** del enunciado (ejercicios con curl sobre Wikidata) se hace antes o en paralelo; a partir de la **Parte 2** usás este proyecto (configuración, Swagger, implementación).
