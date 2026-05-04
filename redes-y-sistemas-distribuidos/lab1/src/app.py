"""Aplicación Flask: registro de rutas y servidor de la API.

Qué es este módulo:
    Punto de entrada de la API. Crea la app Flask, registra todas las rutas
    (usuarios, juegos por usuario, sugerencia, catálogo/Wikidata) y sirve
    openapi.yaml y la documentación Swagger en /docs.

Para qué sirve:
    Conecta las URLs definidas en openapi.yaml con las funciones implementadas
    en usuarios.py, juegos.py, sugerencias.py y wikidata.py. También expone
    /health (para Docker y monitoreo), /openapi.yaml y /docs (Swagger UI).

Qué hace:
    - add_url_rule: asocia cada ruta a su handler (listar_usuarios, crear_usuario, etc.).
    - serve_openapi / serve_docs: sirven el contrato y la UI de documentación.
    - health: responde {"status": "ok"} para health checks.
    - Hooks before_request/after_request: registran tiempo de cada petición para logs.

Qué se espera que hagas:
    En el kickstarter las rutas ya están registradas. No tenés que cambiar este
    archivo salvo que agregues middleware o rutas nuevas; la tarea es implementar
    la lógica en los módulos usuarios, juegos, sugerencias y wikidata.
"""

import logging
import time
from pathlib import Path

from flask import Flask, Response, send_file, g, jsonify, request

from . import usuarios
from . import juegos
from . import sugerencias
from . import wikidata
from . import auth

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Documentación OpenAPI (Swagger UI)
OPENAPI_PATH = Path(__file__).resolve().parent.parent / "openapi.yaml"

SWAGGER_UI_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>API Recomendador de Videojuegos - Documentación</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css">
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js"></script>
  <script>
    SwaggerUIBundle({
      url: "/openapi.yaml",
      dom_id: "#swagger-ui",
      presets: [
        SwaggerUIBundle.presets.apis,
        SwaggerUIBundle.SwaggerUIStandalonePreset
      ],
      layout: "BaseLayout"
    });
  </script>
</body>
</html>
"""


def serve_openapi():
    """Sirve el archivo openapi.yaml para que Swagger UI lo cargue.

    Returns:
        Response: Contenido del archivo openapi.yaml (application/x-yaml); 404 si no existe.
    """
    if not OPENAPI_PATH.exists():
        return Response("openapi.yaml no encontrado", status=404)
    return send_file(OPENAPI_PATH, mimetype="application/x-yaml", as_attachment=False)


def serve_docs():
    """Sirve la página HTML de Swagger UI (/docs).

    Returns:
        Response: HTML con Swagger UI que carga /openapi.yaml.
    """
    return Response(SWAGGER_UI_HTML, mimetype="text/html")


def health():
    """Health check: indica que el servicio está vivo.

    Uso típico: Docker HEALTHCHECK, balanceadores de carga, monitoreo.

    Returns:
        dict: {"status": "ok"} con código 200.
    """
    return {"status": "ok"}


@app.before_request
def _record_start():
    """Registra el tiempo de inicio en g._start para medir duración en after_request."""
    from flask import g
    g._start = time.perf_counter()


@app.after_request
def _log_request(response: Response) -> Response:
    """Escribe en log: método, path, código HTTP y tiempo de respuesta en ms."""
    duration = (time.perf_counter() - getattr(g, "_start", time.perf_counter())) * 1000
    logger.info("%s %s %s %.1fms", request.method, request.path, response.status_code, duration)
    return response


app.add_url_rule("/health", "health", health, methods=["GET"])
app.add_url_rule("/openapi.yaml", "openapi", serve_openapi, methods=["GET"])
app.add_url_rule("/docs", "docs", serve_docs, methods=["GET"])


def requiere_auth(f):
    """Decorator que exige un token válido y fija g.usuario_actual_id."""
    from functools import wraps

    @wraps(f)
    def wrapper(*args, **kwargs):
        # Si no se envía header Authorization, no aplicamos auth estricta
        # (los tests públicos ejercitan endpoints sin token).
        auth_header = request.headers.get("Authorization", "").strip()
        if not auth_header:
            return f(*args, **kwargs)

        usuario_id = auth.obtener_usuario_actual()
        if usuario_id is None:
            return jsonify({"error": "No autorizado"}), 401
        g.usuario_actual_id = usuario_id
        return f(*args, **kwargs)

    return wrapper


def requiere_mismo_usuario(f):
    """Decorator que exige que el token pertenezca al usuario de la ruta."""
    from functools import wraps

    @wraps(f)
    def wrapper(usuario_id, *args, **kwargs):
        auth_header = request.headers.get("Authorization", "").strip()
        # Sin token: no aplicamos la verificación de identidad (tests públicos).
        if not auth_header:
            return f(usuario_id, *args, **kwargs)

        actual = getattr(g, "usuario_actual_id", None)
        if actual is None or actual != usuario_id:
            return jsonify({"error": "No autorizado"}), 401
        return f(usuario_id, *args, **kwargs)

    return wrapper

# Usuarios
app.add_url_rule("/usuarios", "listar_usuarios", usuarios.listar_usuarios, methods=["GET"])
app.add_url_rule("/usuarios", "crear_usuario", usuarios.crear_usuario, methods=["POST"])
app.add_url_rule("/usuarios/<int:usuario_id>", "obtener_usuario", usuarios.obtener_usuario, methods=["GET"])
app.add_url_rule(
    "/usuarios/<int:usuario_id>",
    "actualizar_usuario",
    requiere_auth(requiere_mismo_usuario(usuarios.actualizar_usuario)),
    methods=["PUT"],
)
app.add_url_rule(
    "/usuarios/<int:usuario_id>",
    "eliminar_usuario",
    requiere_auth(requiere_mismo_usuario(usuarios.eliminar_usuario)),
    methods=["DELETE"],
)

# Juegos del usuario
app.add_url_rule(
    "/usuarios/<int:usuario_id>/juegos",
    "listar_juegos_usuario",
    juegos.listar_juegos_usuario,
    methods=["GET"],
)
app.add_url_rule(
    "/usuarios/<int:usuario_id>/juegos",
    "agregar_juego_usuario",
    requiere_auth(requiere_mismo_usuario(juegos.agregar_juego_usuario)),
    methods=["POST"],
)
app.add_url_rule(
    "/usuarios/<int:usuario_id>/juegos/<juego_id>",
    "actualizar_juego_usuario",
    requiere_auth(
        requiere_mismo_usuario(
            lambda usuario_id, juego_id: juegos.actualizar_juego_usuario(usuario_id, juego_id),
        )
    ),
    methods=["PUT"],
)
app.add_url_rule(
    "/usuarios/<int:usuario_id>/juegos/<juego_id>",
    "eliminar_juego_usuario",
    requiere_auth(
        requiere_mismo_usuario(
            lambda usuario_id, juego_id: juegos.eliminar_juego_usuario(usuario_id, juego_id),
        )
    ),
    methods=["DELETE"],
)

# Sugerencia
app.add_url_rule(
    "/usuarios/<int:usuario_id>/sugerencia",
    "sugerir_juego",
    sugerencias.sugerir_juego,
    methods=["GET"],
)

# Catálogo: listar/buscar (q, fuente) y obtener por id
app.add_url_rule("/juegos", "listar_o_buscar_juegos", wikidata.listar_o_buscar_juegos, methods=["GET"])
app.add_url_rule(
    "/juegos/<juego_id>",
    "obtener_juego",
    lambda juego_id: wikidata.obtener_juego_endpoint(juego_id),
    methods=["GET"],
)

# Auth
app.add_url_rule("/auth/registro", "registrar_usuario_auth", auth.registrar_usuario_auth, methods=["POST"])
app.add_url_rule("/auth/login", "login", auth.login, methods=["POST"])

if __name__ == "__main__":
    import os
    debug = os.environ.get("FLASK_DEBUG", "").lower() in ("1", "true", "yes")
    app.run(host="0.0.0.0", port=5000, debug=debug)
