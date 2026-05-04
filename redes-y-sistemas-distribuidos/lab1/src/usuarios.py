"""CRUD de usuarios (crear, listar, obtener, actualizar, eliminar).

Qué es este módulo:
    Implementa los endpoints de la API relacionados con usuarios: GET/POST /usuarios
    y GET/PUT/DELETE /usuarios/<id>. Los datos se guardan en store.USUARIOS y
    store.LISTAS_JUEGOS (cada usuario tiene una lista de juegos asociada).

Para qué sirve:
    Permite que los clientes registren usuarios y que luego puedan asociarles
    listas de juegos (en el módulo juegos.py).

Qué hace:
    - listar_usuarios: devuelve todos los usuarios.
    - obtener_usuario: devuelve un usuario por id o 404.
    - crear_usuario: crea uno con nombre (body JSON); inicializa su lista vacía.
    - actualizar_usuario: actualiza el nombre; 404 si no existe.
    - eliminar_usuario: borra el usuario y su lista; 404 si no existe.

Qué se espera que hagas:
    En el kickstarter las funciones vienen con stubs (501). Tenés que implementar
    la lógica usando store.USUARIOS, store.LISTAS_JUEGOS y next_usuario_id(),
    y devolver los códigos HTTP y cuerpos indicados en openapi.yaml (400, 404, 201, etc.).
"""

from flask import request, jsonify

from .store import USUARIOS, LISTAS_JUEGOS, next_usuario_id, _persist_listas, _persist_usuarios


def listar_usuarios():
    """Lista todos los usuarios registrados.

    Returns:
        Response: JSON con la lista de usuarios (cada uno con id y nombre).
        Código 200.
    """
    
    return jsonify(USUARIOS), 200


def obtener_usuario(usuario_id: int):
    """Obtiene un usuario por su id.

    Args:
        usuario_id: Id numérico del usuario.

    Returns:
        Response: JSON del usuario (id, nombre) si existe; 200.
        Si no existe: JSON con error y código 404.
    """
    usuario = next((u for u in USUARIOS if u["id"] == usuario_id), None)
    if usuario is None: 
        return jsonify({"error": "id de usuario no encontrada"}), 404 
    return jsonify(usuario), 200


def crear_usuario():
    """Crea un nuevo usuario. El body debe incluir "nombre".

    Request body (JSON):
        nombre (str, obligatorio): nombre del usuario.

    Returns:
        Response: JSON del usuario creado (id, nombre) y código 201.
        Si falta nombre o body inválido: JSON error y 400.
    """
    if not request.json or "nombre" not in request.json:
        return jsonify({"error": "Datos inválidos: se requiere nombre"}), 400
    nombre = request.json["nombre"]
    usuario = {
        "id": next_usuario_id(),
        "nombre": nombre,
    }
    USUARIOS.append(usuario)
    LISTAS_JUEGOS[usuario["id"]] = []
    _persist_usuarios()
    _persist_listas()
    return jsonify(usuario), 201


def actualizar_usuario(usuario_id: int):
    """Actualiza los datos de un usuario (típicamente el nombre).

    Args:
        usuario_id: Id del usuario a actualizar.

    Request body (JSON):
        nombre (str, opcional): nuevo nombre.

    Returns:
        Response: JSON del usuario actualizado y 200; 404 si no existe, 400 si body inválido.
    """
    usuario = next((u for u in USUARIOS if u["id"] == usuario_id), None)
    if usuario is None:
        return jsonify({"error": "id de usuario no encontrada"}), 404
    if not request.json or "nombre" not in request.json:
        return jsonify({"error": "Datos inválidos: se requiere nombre"}), 400
    nombre = request.json["nombre"]
    usuario["nombre"] = nombre
    _persist_usuarios()
    _persist_listas()
    return jsonify(usuario), 200


def eliminar_usuario(usuario_id: int):
    """Elimina un usuario y su lista de juegos asociada.

    Args:
        usuario_id: Id del usuario a eliminar.

    Returns:
        Response: JSON con mensaje de éxito y 200; 404 si el usuario no existe.
    """
    
    usuario = next((u for u in USUARIOS if u["id"] == usuario_id), None)
    if usuario is None:
        return jsonify({"error": "id de usuario no encontrada"}), 404
    
    USUARIOS.remove(usuario)
    
    if usuario_id in LISTAS_JUEGOS:
        del LISTAS_JUEGOS[usuario_id]
    _persist_usuarios()
    _persist_listas()
    
    return jsonify({"mensaje": "Usuario eliminado correctamente"}), 200
