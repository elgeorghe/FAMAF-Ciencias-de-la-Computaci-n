"""Helpers compartidos para autenticación (registro, login y tokens).

Este módulo NO decide cómo se guarda la contraseña ni cómo se maneja la
expiración de tokens; eso queda a cargo de `auth.py` (seguro) y
`auth_kickstart.py` (versión insegura para el kickstarter).
"""

from __future__ import annotations

from typing import Any, Dict, Tuple

from flask import jsonify, request

from .store import (
    USUARIOS,
    obtener_credenciales_por_username,
    obtener_usuario_por_token,
    next_usuario_id,
    _persist_usuarios,
)


def parse_register_body() -> Tuple[Dict[str, str] | None, tuple[Any, int] | None]:
    """Parsea el body de registro y valida campos obligatorios.

    Returns:
        (data, None) si es válido, donde data tiene username, nombre, password.
        (None, (response, status)) si hay error (400).
    """
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    nombre = (data.get("nombre") or "").strip()
    password = data.get("password") or ""
    if not username or not nombre or not password:
        return None, (jsonify({"error": "Datos inválidos"}), 400)
    return {"username": username, "nombre": nombre, "password": password}, None


def ensure_username_unique(username: str) -> tuple[Any, int] | None:
    """Devuelve error 409 si el username ya existe, o None si es único."""
    if obtener_credenciales_por_username(username) is not None:
        return jsonify({"error": "Username ya existe"}), 409
    return None


def crear_usuario_basico(nombre: str) -> dict:
    """Crea un usuario en memoria/DB y lo devuelve."""
    usuario_id = next_usuario_id()
    usuario = {"id": usuario_id, "nombre": nombre}
    USUARIOS.append(usuario)
    _persist_usuarios()
    return usuario


def parse_login_body() -> Tuple[Dict[str, str] | None, tuple[Any, int] | None]:
    """Parsea body de login y valida credenciales mínimas.

    Returns:
        (data, None) con username/password si es válido.
        (None, (response, status)) con error 401 si falta algo.
    """
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""
    if not username or not password:
        return None, (jsonify({"error": "Credenciales inválidas"}), 401)
    return {"username": username, "password": password}, None


def get_credenciales_or_401(username: str) -> tuple[dict[str, Any] | None, tuple[Any, int] | None]:
    """Obtiene credenciales por username o devuelve error 401 si no existen."""
    cred = obtener_credenciales_por_username(username)
    if cred is None:
        return None, (jsonify({"error": "Credenciales inválidas"}), 401)
    return cred, None


def extraer_token_de_header() -> str | None:
    """Obtiene el token del header Authorization: Token <TOKEN>."""
    auth_header = request.headers.get("Authorization", "").strip()
    if not auth_header:
        return None
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "token":
        return None
    return parts[1]


def obtener_datos_token(token: str) -> dict[str, Any] | None:
    """Wrapper sobre store.obtener_usuario_por_token."""
    return obtener_usuario_por_token(token)

