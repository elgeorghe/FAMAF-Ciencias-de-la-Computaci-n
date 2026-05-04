"""Filtrado por género y ordenación (asc/desc) para listados de juegos.

Qué es este módulo:
    Proporciona la función filtrar_y_ordenar, usada tanto para la lista de
    juegos de un usuario (juegos.py) como para el catálogo global (wikidata.py).

Para qué sirve:
    Evita duplicar la lógica de "filtrar por género" y "ordenar por campo X
    ascendente o descendente" en varios lugares. Un solo lugar para mantener
    el comportamiento consistente.

Qué hace:
    - filtrar_y_ordenar: recibe una lista de diccionarios (juegos), opcionalmente
      filtra por genero y ordena por el campo indicado (nombre, lanzamiento, id, etc.)
      en orden asc o desc. Devuelve una nueva lista (no muta la original).
    - ORDEN_VALIDOS_CATALOGO y ORDEN_VALIDOS_LISTA: tuplas de valores permitidos
      para el parámetro ordenar en cada contexto.

Qué se espera que hagas:
    En el kickstarter este módulo ya viene implementado. No es necesario
    modificarlo; usalo desde juegos.py (listar_juegos_usuario) y wikidata.py
    (listar_o_buscar_juegos) pasando los query params genero, ordenar y orden.
"""

ORDEN_VALIDOS_CATALOGO = ("id", "nombre", "lanzamiento", "genero")
ORDEN_VALIDOS_LISTA = ("nombre", "fecha_lanzamiento", "fecha_agregado")


def _normalizar_orden_campo(
    ordenar: str, orden: str, ordenes_validos: tuple[str, ...]
) -> tuple[str, str, bool]:
    """Normaliza ordenar y orden para usarlos en sort.

    Args:
        ordenar: Nombre del campo por el que ordenar (p. ej. "nombre", "fecha_lanzamiento").
        orden: "asc" o "desc".
        ordenes_validos: Valores permitidos para ordenar; si ordenar no está, se usa el primero.

    Returns:
        Tupla (ordenar_final, campo_orden, reverse). reverse=True si orden es "desc".
    """
    orden_safe = orden if orden in ("asc", "desc") else "asc"
    reverse = orden_safe == "desc"
    if ordenes_validos and ordenar not in ordenes_validos:
        ordenar = ordenes_validos[0] if ordenes_validos else "id"
    campo = "lanzamiento" if ordenar == "fecha_lanzamiento" else ordenar
    return (ordenar, campo, reverse)


def _clave_orden(campo: str):
    """Devuelve una función key para usar en list.sort según el campo.

    Args:
        campo: Nombre del campo (nombre, lanzamiento, id, etc.).

    Returns:
        Función que recibe un dict (ítem de juego) y devuelve el valor por el que ordenar.
    """
    if campo == "nombre":
        return lambda x: (x.get("nombre") or "").lower()
    return lambda x: x.get(campo) or ""


def filtrar_y_ordenar(
    items: list[dict],
    *,
    genero: str | None = None,
    ordenar: str = "id",
    orden: str = "asc",
    ordenes_validos: tuple[str, ...] = (),
) -> list[dict]:
    """Filtra por género (si se indica) y ordena la lista por el campo dado.

    No modifica la lista original; devuelve una nueva lista.

    Args:
        items: Lista de diccionarios (cada uno con campos como nombre, genero, lanzamiento, etc.).
        genero: Si se pasa, solo se mantienen ítems cuyo campo "genero" coincida.
        ordenar: Campo por el que ordenar (nombre, lanzamiento, genero, id, fecha_agregado;
                 "fecha_lanzamiento" se mapea a "lanzamiento").
        orden: "asc" o "desc".
        ordenes_validos: Si se pasa, ordenar debe estar en esta tupla; si no, se usa el primer valor.

    Returns:
        Nueva lista filtrada y ordenada.
    """
    result = list(items)
    if genero and genero.strip():
        result = [i for i in result if (i.get("genero") or "") == genero]
    _, campo, reverse = _normalizar_orden_campo(ordenar, orden, ordenes_validos)
    result.sort(key=_clave_orden(campo), reverse=reverse)
    return result
