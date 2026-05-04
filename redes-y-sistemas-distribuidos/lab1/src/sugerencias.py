"""Sugerencia de un juego al azar desde la lista del usuario (opcional por género).

Qué es este módulo:
    Implementa el endpoint GET /usuarios/<id>/sugerir que devuelve un juego
    elegido al azar entre los que el usuario tiene (tengo=true), opcionalmente
    filtrado por género.

Para qué sirve:
    Dar una recomendación aleatoria al usuario basada en lo que ya tiene,
    útil para “¿qué juego juego hoy?” o para descubrir uno por género.

Qué hace:
    - _candidatos_que_tengo: obtiene los ítems con tengo=true del usuario.
    - _filtrar_candidatos_por_genero: filtra por género usando el catálogo.
    - _candidatos_sugerencia: combina ambos; None si el usuario no existe.
    - sugerir_juego: el endpoint; 404 si usuario no existe o no hay candidatos.

Qué se espera que hagas:
    En el kickstarter la lógica de sugerir_juego viene con stub. Implementá
    usando las helpers _candidatos_sugerencia y el catálogo para enriquecer
    el JSON de respuesta (id, nombre, descripcion, genero, lanzamiento, plataforma).
"""

import random
from flask import request, jsonify

from src.wikidata import obtener_juego
from .usuarios import obtener_usuario
from .store import USUARIOS, LISTAS_JUEGOS, CATALOGO_JUEGOS

def _candidatos_que_tengo(usuario_id: int) -> list[dict] | None:
    """Devuelve los ítems de la lista del usuario con tengo=true.

    Args:
        usuario_id: Id del usuario.

    Returns:
        Lista de ítems (dict con juego_id, flags, etc.); None si el usuario no existe.
    """
    if next((x for x in USUARIOS if x["id"] == usuario_id), None) is None:
        return None
    lista = LISTAS_JUEGOS.get(usuario_id, [])
    return [i for i in lista if i.get("tengo")]


def _filtrar_candidatos_por_genero(candidatos: list[dict], genero: str | None) -> list[dict]:
    """Filtra la lista de candidatos por género según el catálogo.

    Args:
        candidatos: Lista de ítems (con juego_id).
        genero: Género a filtrar; si es None, devuelve todos los candidatos.

    Returns:
        Lista de ítems cuyo juego tiene ese género en el catálogo.
    """
    if not genero:
        return candidatos
    return [
        i for i in candidatos
        if CATALOGO_JUEGOS.get(i["juego_id"], {}).get("genero") == genero
    ]


def _candidatos_sugerencia(usuario_id: int, genero: str | None) -> list[dict] | None:
    """Obtiene candidatos para sugerir: ítems con tengo=true, opcionalmente por género.

    Args:
        usuario_id: Id del usuario.
        genero: Género opcional para filtrar; None = todos.

    Returns:
        Lista de ítems candidatos; None si el usuario no existe.
    """
    candidatos = _candidatos_que_tengo(usuario_id)
    if candidatos is None:
        return None
    return _filtrar_candidatos_por_genero(candidatos, genero)


def sugerir_juego(usuario_id: int):
    """Sugiere un juego al azar entre los que el usuario tiene (tengo=true).

    Query param: genero (opcional) para filtrar por género.

    Args:
        usuario_id: Id del usuario.

    Returns:
        Response: JSON con id, nombre, descripcion, genero, lanzamiento, plataforma y 200;
        404 si el usuario no existe o no hay juegos que cumplan el criterio.
    """
    usuario = obtener_usuario(usuario_id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    genero = request.args.get("genero")
    candidatos = _candidatos_sugerencia(usuario_id, genero)
    if not candidatos:
        return jsonify({"error": "No hay juegos que cumplan el criterio"}), 404
    juego_rel = random.choice(candidatos)

    info = obtener_juego(juego_rel["juego_id"])

    return jsonify({
        "id": juego_rel["juego_id"],
        "nombre": info.get("nombre"),
        "descripcion": info.get("descripcion"),
        "genero": info.get("genero"),
        "lanzamiento": info.get("lanzamiento"),
        "plataforma": info.get("plataforma"),
    }), 200
    return jsonify(juego_rel), 200
