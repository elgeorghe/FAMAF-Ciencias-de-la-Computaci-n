"""Almacén con persistencia SQLite para usuarios, catálogo de juegos y listas por usuario.

Qué es este módulo:
    Centraliza las estructuras de datos que usa la API: usuarios, catálogo de juegos
    (poblado desde Wikidata) y la lista de juegos de cada usuario. Los datos se
    persisten en SQLite (por defecto instance/datos.db; variable LAB1_DATABASE).

Para qué sirve:
    Evita duplicar datos entre módulos; usuarios.py, juegos.py, sugerencias.py
    y wikidata.py leen y modifican estas estructuras. La persistencia es
    transparente: mismo API (USUARIOS, LISTAS_JUEGOS, CATALOGO_JUEGOS, next_usuario_id).

Qué hace:
    - Al importar: crea tablas si no existen y carga desde la DB en memoria.
    - USUARIOS, LISTAS_JUEGOS, CATALOGO_JUEGOS y next_usuario_id() como siempre.
    - Tras cambios, los módulos llaman _persist_usuarios(), _persist_listas(),
      _persist_catalogo() o _persist_next_id() para guardar en SQLite.

Qué se espera que hagas:
    En el kickstarter este módulo ya viene implementado. No tenés que modificarlo.
    Para volver a empezar con datos vacíos: make clean-db.
"""

import os
import sqlite3
from pathlib import Path
from typing import Any

_DB_PATH: str | None = None


def _db_path() -> str:
    """Ruta del archivo SQLite (LAB1_DATABASE o por defecto instance/datos.db)."""
    global _DB_PATH
    if _DB_PATH is None:
        _DB_PATH = os.environ.get("LAB1_DATABASE", "instance/datos.db")
        if not os.path.isabs(_DB_PATH):
            _DB_PATH = os.path.abspath(_DB_PATH)
    return _DB_PATH


def _get_conn() -> sqlite3.Connection:
    """Abre una conexión a la base SQLite."""
    path = _db_path()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(path)


def _init_db() -> None:
    """Crea las tablas si no existen."""
    conn = _get_conn()
    try:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS listas_juegos (
                usuario_id INTEGER NOT NULL,
                juego_id TEXT NOT NULL,
                tengo INTEGER NOT NULL,
                quiero INTEGER NOT NULL,
                jugado INTEGER NOT NULL,
                me_gusta INTEGER NOT NULL,
                fecha_agregado TEXT NOT NULL,
                PRIMARY KEY (usuario_id, juego_id)
            );
            CREATE TABLE IF NOT EXISTS catalogo (
                juego_id TEXT PRIMARY KEY,
                nombre TEXT,
                genero TEXT,
                lanzamiento TEXT,
                plataforma TEXT,
                descripcion TEXT
            );
            CREATE TABLE IF NOT EXISTS meta (
                key TEXT PRIMARY KEY,
                value TEXT
            );
            CREATE TABLE IF NOT EXISTS credenciales (
                usuario_id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                token TEXT,
                token_expira_en TEXT
            );
        """)
        conn.commit()
    finally:
        conn.close()


def _load_usuarios_from_cur(cur: sqlite3.Cursor) -> None:
    """Carga USUARIOS desde el cursor (SELECT id, nombre FROM usuarios)."""
    global USUARIOS
    USUARIOS[:] = [{"id": row["id"], "nombre": row["nombre"]} for row in cur.fetchall()]


def _load_listas_from_cur(cur: sqlite3.Cursor) -> None:
    """Carga LISTAS_JUEGOS desde el cursor (tabla listas_juegos)."""
    global LISTAS_JUEGOS
    for row in cur.fetchall():
        uid = row["usuario_id"]
        if uid not in LISTAS_JUEGOS:
            LISTAS_JUEGOS[uid] = []
        LISTAS_JUEGOS[uid].append({
            "juego_id": row["juego_id"],
            "tengo": bool(row["tengo"]),
            "quiero": bool(row["quiero"]),
            "jugado": bool(row["jugado"]),
            "me_gusta": bool(row["me_gusta"]),
            "fecha_agregado": row["fecha_agregado"] or "",
        })


def _load_catalogo_from_cur(cur: sqlite3.Cursor) -> None:
    """Carga CATALOGO_JUEGOS desde el cursor (tabla catalogo)."""
    global CATALOGO_JUEGOS
    for row in cur.fetchall():
        CATALOGO_JUEGOS[row["juego_id"]] = {
            "id": row["juego_id"],
            "nombre": row["nombre"] or "",
            "genero": row["genero"] or "",
            "lanzamiento": row["lanzamiento"] or "",
            "plataforma": row["plataforma"] or "",
            "descripcion": row["descripcion"] or "",
        }


def _load_next_id_from_cur(cur: sqlite3.Cursor) -> None:
    """Carga _next_usuario_id desde el cursor (meta) o desde max(USUARIOS)."""
    global _next_usuario_id
    row = cur.fetchone()
    if row is not None and row["value"].isdigit():
        _next_usuario_id = int(row["value"])
    elif USUARIOS:
        _next_usuario_id = max(u["id"] for u in USUARIOS) + 1


def _load_from_db() -> None:
    """Carga USUARIOS, LISTAS_JUEGOS, CATALOGO_JUEGOS y _next_usuario_id desde la DB."""
    conn = _get_conn()
    conn.row_factory = sqlite3.Row
    try:
        _load_usuarios_from_cur(conn.execute("SELECT id, nombre FROM usuarios ORDER BY id"))
        _load_listas_from_cur(conn.execute(
            "SELECT usuario_id, juego_id, tengo, quiero, jugado, me_gusta, fecha_agregado FROM listas_juegos"
        ))
        _load_catalogo_from_cur(conn.execute(
            "SELECT juego_id, nombre, genero, lanzamiento, plataforma, descripcion FROM catalogo"
        ))
        _load_next_id_from_cur(conn.execute("SELECT value FROM meta WHERE key = 'next_usuario_id'"))
    finally:
        conn.close()


# Usuarios: lista de dict con id, nombre
USUARIOS: list[dict[str, Any]] = []

# Catálogo: id Wikidata (Q-id) -> juego mapeado
CATALOGO_JUEGOS: dict[str, dict[str, Any]] = {}

# Listas por usuario_id: cada ítem tiene juego_id, tengo, quiero, jugado, me_gusta, fecha_agregado
LISTAS_JUEGOS: dict[int, list[dict[str, Any]]] = {}

_next_usuario_id = 1

_init_db()
_load_from_db()


def guardar_credenciales(usuario_id: int, username: str, password_hash: str) -> None:
    """Crea o actualiza las credenciales básicas (sin token) de un usuario."""
    conn = _get_conn()
    try:
        conn.execute(
            """
            INSERT INTO credenciales (usuario_id, username, password_hash)
            VALUES (?, ?, ?)
            ON CONFLICT(username) DO UPDATE SET
                usuario_id = excluded.usuario_id,
                password_hash = excluded.password_hash
            """,
            (usuario_id, username, password_hash),
        )
        conn.commit()
    finally:
        conn.close()


def obtener_credenciales_por_username(username: str) -> dict[str, Any] | None:
    """Devuelve un dict con las credenciales de un username o None si no existe."""
    conn = _get_conn()
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.execute(
            """
            SELECT usuario_id, username, password_hash, token, token_expira_en
            FROM credenciales
            WHERE username = ?
            """,
            (username,),
        )
        row = cur.fetchone()
        if row is None:
            return None
        return {
            "usuario_id": row["usuario_id"],
            "username": row["username"],
            "password_hash": row["password_hash"],
            "token": row["token"],
            "token_expira_en": row["token_expira_en"],
        }
    finally:
        conn.close()


def actualizar_token(usuario_id: int, token: str, expira_en: str) -> None:
    """Actualiza el token y la expiración para un usuario ya registrado."""
    conn = _get_conn()
    try:
        conn.execute(
            """
            UPDATE credenciales
            SET token = ?, token_expira_en = ?
            WHERE usuario_id = ?
            """,
            (token, expira_en, usuario_id),
        )
        conn.commit()
    finally:
        conn.close()


def obtener_usuario_por_token(token: str) -> dict[str, Any] | None:
    """Devuelve usuario_id y token_expira_en asociados a un token, o None si no existe."""
    conn = _get_conn()
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.execute(
            """
            SELECT usuario_id, token_expira_en
            FROM credenciales
            WHERE token = ?
            """,
            (token,),
        )
        row = cur.fetchone()
        if row is None:
            return None
        return {
            "usuario_id": row["usuario_id"],
            "token_expira_en": row["token_expira_en"],
        }
    finally:
        conn.close()


def _persist_usuarios() -> None:
    """Guarda USUARIOS en la base SQLite."""
    conn = _get_conn()
    try:
        conn.execute("DELETE FROM usuarios")
        for u in USUARIOS:
            conn.execute("INSERT INTO usuarios (id, nombre) VALUES (?, ?)", (u["id"], u.get("nombre", "")))
        conn.commit()
    finally:
        conn.close()


def _persist_listas() -> None:
    """Guarda LISTAS_JUEGOS en la base SQLite."""
    conn = _get_conn()
    try:
        conn.execute("DELETE FROM listas_juegos")
        for uid, items in LISTAS_JUEGOS.items():
            for it in items:
                conn.execute(
                    "INSERT INTO listas_juegos (usuario_id, juego_id, tengo, quiero, jugado, me_gusta, fecha_agregado) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (
                        uid,
                        it.get("juego_id", ""),
                        1 if it.get("tengo") else 0,
                        1 if it.get("quiero") else 0,
                        1 if it.get("jugado") else 0,
                        1 if it.get("me_gusta") else 0,
                        it.get("fecha_agregado", "") or "",
                    ),
                )
        conn.commit()
    finally:
        conn.close()


def _persist_catalogo() -> None:
    """Guarda CATALOGO_JUEGOS en la base SQLite."""
    conn = _get_conn()
    try:
        conn.execute("DELETE FROM catalogo")
        for jid, j in CATALOGO_JUEGOS.items():
            conn.execute(
                "INSERT INTO catalogo (juego_id, nombre, genero, lanzamiento, plataforma, descripcion) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    jid,
                    j.get("nombre", "") or "",
                    j.get("genero", "") or "",
                    j.get("lanzamiento", "") or "",
                    j.get("plataforma", "") or "",
                    j.get("descripcion", "") or "",
                ),
            )
        conn.commit()
    finally:
        conn.close()


def _persist_next_id() -> None:
    """Guarda _next_usuario_id en la tabla meta."""
    conn = _get_conn()
    try:
        conn.execute(
            "INSERT OR REPLACE INTO meta (key, value) VALUES ('next_usuario_id', ?)",
            (str(_next_usuario_id),),
        )
        conn.commit()
    finally:
        conn.close()


def next_usuario_id() -> int:
    """Genera el próximo id numérico para un nuevo usuario.

    Returns:
        int: Un id único (incremental) para asignar a un usuario recién creado.
    """
    global _next_usuario_id
    n = _next_usuario_id
    _next_usuario_id += 1
    _persist_next_id()
    return n
