"""Versión INSEGURA de autenticación para el kickstarter.

Esta implementación es funcional pero tiene dos problemas graves:

- Guarda las contraseñas en texto plano (password_hash == password).
- No maneja expiración real de tokens (token_expira_en queda en NULL).

El objetivo de la Parte 6 del enunciado es justamente corregir estos
problemas en la solución final.
"""

from __future__ import annotations

import os
from uuid import uuid4

from flask import jsonify

from . import auth_common
from .store import guardar_credenciales, actualizar_token

from .usuarios import obtener_usuario

from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime, timedelta, timezone


def _token_ttl_minutes() -> int:
    """TTL de tokens en minutos (default 60).

    En la versión insegura del kickstarter NO se usa para setear expiración;
    se deja como referencia para los estudiantes.
    """
    raw = os.environ.get("AUTH_TOKEN_TTL_MINUTES", "60")
    try:
        value = int(raw)
    except ValueError:
        return 60
    return max(1, value)


def registrar_usuario_auth():
    """Handler para POST /auth/registro (kickstarter, INSEGURO).

    - Crea el usuario correctamente.
    - Guarda la contraseña en texto plano en password_hash (esto está mal).
    """
    parsed, error = auth_common.parse_register_body()
    if error is not None:
        return error
    assert parsed is not None
    username = parsed["username"]
    nombre = parsed["nombre"]
    password = parsed["password"]

    dup_error = auth_common.ensure_username_unique(username)
    if dup_error is not None:
        return dup_error

    usuario = auth_common.crear_usuario_basico(nombre)

    password_hash = generate_password_hash(password)
    guardar_credenciales(usuario["id"], username, password_hash)

    return jsonify(usuario), 201


def login():
    """Handler para POST /auth/login (kickstarter, INSEGURO).

    - Compara la contraseña en texto plano.
    - Genera un token sin fecha de expiración útil (token_expira_en = NULL).
    """
    parsed, error = auth_common.parse_login_body()
    if error is not None:
        return error
    assert parsed is not None
    username = parsed["username"]
    password = parsed["password"]

    cred, error = auth_common.get_credenciales_or_401(username)
    if error is not None:
        return error
    assert cred is not None

    if not check_password_hash(cred["password_hash"], password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    token = uuid4().hex
    # expiracion en 1 hora por defecto 
    ttl = _token_ttl_minutes()
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=ttl)
    
    actualizar_token(cred["usuario_id"], token, expire_time)

    return jsonify({"token": token}), 200


def obtener_usuario_actual() -> int | None:
    """Devuelve usuario_id asociado al token o None (kickstarter, sin expiración).

    - NO chequea expiración: cualquier token almacenado se considera válido.
    - Esto es inseguro; la solución final debe usar token_expira_en.
    """
    token = auth_common.extraer_token_de_header()
    if not token:
        return None
    data = auth_common.obtener_datos_token(token)
    if data is None:
        return None

    valid_token = data.get("token_expira_en")
    if valid_token is None:
        return None
    
    if isinstance(valid_token, str):
        valid_token = valid_token.replace("Z", "+00:00")
        valid_token = datetime.fromisoformat(valid_token)
    
    if valid_token < datetime.now(timezone.utc):
        return None
    
    usuario_id = data.get("usuario_id")
    return int(usuario_id) if usuario_id is not None else None

def obtener_permisos_usuario(usuario_id):
    user_auth = obtener_usuario_actual()

    if user_auth is None:
        return jsonify({"error": "No autorizado"}), 401

    if user_auth != usuario_id:
        return jsonify({"error": "Prohibido"}), 403

    user = obtener_usuario(usuario_id)
    if user is None:
        return jsonify({"error": "No encontrado"}), 404

    return jsonify(user)