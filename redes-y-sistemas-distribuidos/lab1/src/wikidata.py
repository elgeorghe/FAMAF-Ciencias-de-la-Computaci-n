"""Cliente Wikidata: búsqueda, obtención por id y población del catálogo local.

Qué es este módulo:
    Integración con la API de Wikidata para buscar y obtener videojuegos (Q7889).
    Los resultados se mapean a un formato común (id, nombre, genero, lanzamiento,
    plataforma, descripcion) y se guardan en store.CATALOGO_JUEGOS.

Para qué sirve:
    - Permitir búsqueda de juegos por texto (GET /juegos?q=...&fuente=wikidata).
    - Resolver un juego por Q-id si no está en catálogo (obtener_juego).
    - Poblar/ampliar el catálogo local con datos de Wikidata, usando
      `store.CATALOGO_JUEGOS` como estructura central (análogo a `store.USUARIOS`
      para los usuarios).

Qué hace:
    - buscar(q): busca en Wikidata, filtra videojuegos, mapea y guarda en catálogo; None si falla API.
    - obtener_juego(juego_id): devuelve juego desde catálogo o Wikidata; None si no existe o falla.
    - listar_o_buscar_juegos: GET /juegos (lista catálogo, búsqueda local o wikidata); 502 si falla Wikidata.
    - obtener_juego_endpoint: GET /juegos/<id>; 404 si no encontrado.

Qué se espera que hagas:
    En el kickstarter las funciones públicas pueden venir con stubs. Implementá
    buscar y obtener_juego usando las helpers _request, _mapear_entidad,
    _obtener_labels, etc., y devolved None cuando la API falle; el endpoint
    debe responder 502 cuando buscar devuelve None.
"""

import logging
import os
import requests
from flask import request, jsonify

from .store import CATALOGO_JUEGOS, _persist_catalogo
from . import filtros

logger = logging.getLogger(__name__)

WIKIDATA_BASE = "https://www.wikidata.org/w/api.php"
WIKIDATA_TIMEOUT = 10
VIDEO_GAME_QID = "Q7889"
LANG = "es"
P_DATE = "P577"
P_GENRE = "P136"
P_PLATFORM = "P400"
P_INSTANCE_OF = "P31"


def _get_user_agent() -> str:
    """Devuelve el User-Agent para las peticiones a Wikidata (env WIKIDATA_USER_AGENT o default)."""
    return os.environ.get("WIKIDATA_USER_AGENT", "LabRedes2026/1.0").strip() or "LabRedes2026/1.0"


def _request(params: dict) -> dict | None:
    """Hace GET a la API de Wikidata con los params dados. Añade format=json y User-Agent.

    Args:
        params: Parámetros de query para w/api.php (action, ids, etc.).

    Returns:
        Dict con la respuesta JSON; None si hay error de red, timeout o JSON inválido.
    """
    #formateando a json
    if "format" not in params:
        params["format"] = "json"
    
    headers = {
        "User-Agent": _get_user_agent()
        }
    
    try:
        response = requests.get(
            WIKIDATA_BASE,
            params=params,
            headers=headers,
            timeout=WIKIDATA_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except (requests.exceptions.RequestException, ValueError, KeyError) as e:
        logger.exception(f"Error en request a Wikidata: {e}")
        return None


def _extraer_fecha(time_value: str) -> str:
    """Convierte un valor time de Wikidata (ej. +2020-01-15T00:00:00Z) a string YYYY-MM-DD.

    Args:
        time_value: Valor time tal como viene en claims.

    Returns:
        String de fecha (hasta 10 caracteres) o cadena vacía.
    """
    if not time_value:
        return ""
    s = time_value.replace("T00:00:00Z", "").replace("T00:00:00Z", "").strip()
    if s.startswith("+"):
        s = s[1:]
    return s[:10] if len(s) >= 10 else s


def _obtener_labels(qids: list[str]) -> dict[str, str]:
    """Obtiene los labels (nombres) en español o inglés para una lista de Q-ids.

    Args:
        qids: Lista de Q-ids (máx. 50).

    Returns:
        Dict qid -> valor del label (string).
    """
    if not qids:
        return {}
    
    #la api tiene limite de 50 https://www.wikidata.org/w/api.php?action=help&modules=wbgetentities
    result = {}
    params = {
        "action": "wbgetentities",
        "ids": "|".join(qids),
        "props": "labels",
        "languages": f"{LANG}|en"
    }

    data = _request(params)
    if data is None:
        return {}
    
    entities= data.get("entities", {})
    for qid, ent in entities.items():
        if "missing" in ent:
            continue
        labels = ent.get("labels", {})
        for lang in (LANG, "en"):
            if lang in labels:
                result[qid] = labels[lang].get("value", "")
                break
    return result


def _claim_value_id(claims: dict, prop: str) -> str:
    """Extrae el id (Q-id) del primer claim de una propiedad.

    Args:
        claims: Dict de claims de la entidad.
        prop: Id de propiedad (ej. P136, P400).

    Returns:
        Q-id del valor o cadena vacía.
    """
    if prop not in claims or not claims[prop]:
        return ""
    c = claims[prop][0]
    return c.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("id", "") or ""


def _claim_value_time(claims: dict, prop: str) -> str:
    """Extrae el valor time del primer claim de una propiedad (ej. P577 fecha lanzamiento).

    Args:
        claims: Dict de claims de la entidad.
        prop: Id de propiedad.

    Returns:
        Valor time (string) o cadena vacía.
    """
    if prop not in claims or not claims[prop]:
        return ""
    c = claims[prop][0]
    return c.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("time", "") or ""


def _mapear_entidad(ent: dict, labels_cache: dict[str, str]) -> dict:
    """Convierte una entidad Wikidata a dict juego (id, nombre, genero, lanzamiento, plataforma, descripcion).

    Args:
        ent: Entidad tal como viene de wbgetentities.
        labels_cache: Dict Q-id -> label para resolver género y plataforma.

    Returns:
        Dict con id, nombre, genero, lanzamiento, plataforma, descripcion.
    """
    labels = ent.get("labels", {})
    descriptions = ent.get("descriptions", {})
    claims = ent.get("claims", {})
    qid = ent.get("id", "")
    for lang in (LANG, "en"):
        if lang in labels:
            nombre = labels[lang].get("value", "")
            break
    else:
        nombre = ""
    desc = ""
    for lang in (LANG, "en"):
        if lang in descriptions:
            desc = descriptions[lang].get("value", "")
            break
    lanzamiento = _extraer_fecha(_claim_value_time(claims, P_DATE))
    genero_q = _claim_value_id(claims, P_GENRE)
    plataforma_q = _claim_value_id(claims, P_PLATFORM)
    genero = labels_cache.get(genero_q, "") if genero_q else ""
    plataforma = labels_cache.get(plataforma_q, "") if plataforma_q else ""
    return {
        "id": qid,
        "nombre": nombre,
        "genero": genero,
        "lanzamiento": lanzamiento,
        "plataforma": plataforma,
        "descripcion": desc,
    }


def _es_videojuego(ent: dict) -> bool:
    """Indica si la entidad tiene P31=Q7889 (instance of video game).

    Args:
        ent: Entidad Wikidata (con claims).

    Returns:
        True si es videojuego, False si no.
    """
    #encontre esto sobre los claims https://www.wikidata.org/wiki/Help:Wikidata_datamodel
    claims = ent.get("claims", {})
    instance_of = claims.get(P_INSTANCE_OF, [])

    for claim in instance_of:
        mainsnak = claim.get("mainsnak", {})
        
        datavalue = mainsnak.get("datavalue", {})
        value = datavalue.get("value", {})
        if isinstance(value, dict):
            if value.get("id") == VIDEO_GAME_QID:
                return True
            elif value == VIDEO_GAME_QID:
                return True
    return False


def _buscar_ids_wikidata(q: str) -> list[str] | None:
    """Busca entidades en Wikidata por texto y devuelve sus ids.

    Args:
        q: Texto de búsqueda.

    Returns:
        Lista de Q-ids encontrados; None si falla la API; [] si sin resultados.
    """
    params = {
        "action": "wbsearchentities",
        "search": q,
        "language": LANG
    }

    data = _request(params)
    if data is None:
        return None

    search_results = data.get("search", [])
    return [item.get("id") for item in search_results if item.get("id")]


def _filtrar_ids_videojuegos(ids: list[str]) -> list[str] | None:
    """Filtra la lista de ids dejando solo los que son videojuegos (P31=Q7889).

    Args:
        ids: Lista de Q-ids a comprobar.

    Returns:
        Lista de ids que son videojuegos; None si falla la API; [] si ninguno.
    """
    if not ids:
        return []
    
    params = {
        "action": "wbgetentities",
        "ids": "|".join(ids),
        "props": "claims"
    }

    data = _request(params)
    if data is None:
        return None
    
    entities = data.get("entities", {})
    video_game_ids = []

    for qid, ent in entities.items():
        if "missing" in ent:
            continue
        if _es_videojuego(ent):
            video_game_ids.append(qid)

    return video_game_ids


def _entidades_completas_videojuegos(video_game_ids: list[str]) -> dict | None:
    """Obtiene entidades completas (labels, descriptions, claims) para los ids dados.

    Args:
        video_game_ids: Lista de Q-ids de videojuegos.

    Returns:
        Dict qid -> entidad; None si falla la API; {} si la lista está vacía.
    """
    if not video_game_ids:
        return {}
    
    params = {
        "action": "wbgetentities",
        "ids": "|".join(video_game_ids),
        "props": "labels|descriptions|claims",
        "languages": f"{LANG}|en"
    }

    data = _request(params)
    if data is None:
        return None
    
    return data.get("entities", {})


def _colectar_ref_qids(entities: dict) -> set:
    """Extrae los Q-ids de género (P136) y plataforma (P400) de las entidades.

    Args:
        entities: Dict qid -> entidad con claims.

    Returns:
        Set de Q-ids a resolver para labels (genero, plataforma).
    """
    ref_qids = set()
    for ent in entities.values():
        if "missing" in ent:
            continue
        claims = ent.get("claims", {})
        for q in (_claim_value_id(claims, P_GENRE), _claim_value_id(claims, P_PLATFORM)):
            if q:
                ref_qids.add(q)
    return ref_qids


def _mapear_y_guardar_resultados(
    video_game_ids: list[str], entities: dict, labels_cache: dict[str, str]
) -> list[dict]:
    """Mapea entidades a formato juego, las guarda en CATALOGO_JUEGOS y devuelve la lista.

    Args:
        video_game_ids: Orden de ids a incluir.
        entities: Dict qid -> entidad.
        labels_cache: Dict Q-id -> label para género/plataforma.

    Returns:
        Lista de dicts de juegos (id, nombre, genero, etc.); se omiten entidades missing.
    """
    resultados = []
    for qid in video_game_ids:
        ent = entities.get(qid, {})
        if "missing" in ent:
            continue
        ent = dict(ent)
        ent["id"] = qid
        juego = _mapear_entidad(ent, labels_cache)
        CATALOGO_JUEGOS[qid] = juego
        resultados.append(juego)
    _persist_catalogo()
    return resultados


def buscar(q: str) -> list[dict] | None:
    """Busca en Wikidata por texto, filtra videojuegos, mapea y guarda en catálogo.

    Args:
        q: Texto de búsqueda.

    Returns:
        Lista de juegos (dict con id, nombre, genero, etc.); None si falla la API;
        [] si no hay resultados o ninguno es videojuego.
    """
    #busqueda de ids por texto
    ids = _buscar_ids_wikidata(q)
    if ids is None:
        return None
    if not ids:
        return []
    
    #filtrando los juegos
    video_game_ids = _filtrar_ids_videojuegos(ids)
    if video_game_ids is None:
        return None
    if not video_game_ids:
        return []
    
    #hacen falta entities completas? revisar
    entities = _entidades_completas_videojuegos(video_game_ids)
    if entities is None:
        return None
    if not entities:
        return []
    
    #sacando labels
    ref_qids = _colectar_ref_qids(entities)
    labels_cache = _obtener_labels(list(ref_qids)) if ref_qids else {}

    return _mapear_y_guardar_resultados(video_game_ids, entities, labels_cache)


def obtener_juego(juego_id: str) -> dict | None:
    """Obtiene un juego por Q-id: primero catálogo local, si no está consulta Wikidata y guarda.

    Args:
        juego_id: Q-id del juego (ej. Q12345).

    Returns:
        Dict del juego (id, nombre, genero, lanzamiento, plataforma, descripcion);
        None si no existe o falla la API.
    """
    #ver si ya esta en catalogo
    if juego_id in CATALOGO_JUEGOS:
        return CATALOGO_JUEGOS[juego_id]
    
    #no esta en catalogo, request a wikidata
    entities = _entidades_completas_videojuegos([juego_id])
    if entities is None or not entities:
        return None
    
    ent = entities.get(juego_id)
    if not ent or "missing" in ent:
        return None
    
    #chekeo si es juego por si acaso
    if not _es_videojuego(ent):
        return None
    
    #labels
    ref_qids = _colectar_ref_qids({juego_id: ent})
    labels_cache = _obtener_labels(list(ref_qids)) if ref_qids else {}

    #mapeado y guardado
    juego = _mapear_entidad(ent, labels_cache)
    CATALOGO_JUEGOS[juego_id] = juego
    _persist_catalogo()

    return juego

def _obtener_lista_juegos_para_get() -> tuple[list[dict] | None, tuple | None]:
    """Resuelve la lista de juegos para GET /juegos según query params q y fuente.

    Sin q: devuelve todo el catálogo. Con q y fuente=local: filtra por nombre en catálogo.
    Con q y fuente=wikidata: llama a buscar(q); si falla devuelve error 502.

    Returns:
        (lista, None) con la lista de juegos a devolver; o (None, (response, 502)) si falla Wikidata.
    """
    q = request.args.get("q", "").strip()
    fuente = request.args.get("fuente", "local").strip().lower()
    if not q:
        return list(CATALOGO_JUEGOS.values()), None
    if fuente == "wikidata":
        resultados = buscar(q)
        if resultados is None:
            return None, (jsonify({"error": "Error al consultar Wikidata"}), 502)
        return list(resultados or []), None
    q_lower = q.lower()
    return [j for j in CATALOGO_JUEGOS.values() if q_lower in (j.get("nombre") or "").lower()], None


def listar_o_buscar_juegos():
    """Handler GET /juegos: listar catálogo o buscar por q con fuente local o wikidata.

    Query params: q (opcional), fuente (local|wikidata), genero, ordenar, orden.

    Returns:
        Response: JSON con lista de juegos y 200; 502 si fuente=wikidata y falla la API.
    """
    lista_juegos, error = _obtener_lista_juegos_para_get()
    if error is not None:
        return error
    
    #filtrable por genero y orden, articulo sobre filtrado: https://www.geeksforgeeks.org/python/using-request-args-for-a-variable-url-in-flask/
    genero = request.args.get("genero", "").strip() or None
    ordenar = request.args.get("ordenar", "id")
    orden = request.args.get("orden", "asc")
    
    #usar filtros de .filtros
    resultado = filtros.filtrar_y_ordenar(
        lista_juegos,
        genero=genero,
        ordenar=ordenar,
        orden=orden,
        ordenes_validos=filtros.ORDEN_VALIDOS_CATALOGO
    )

    return jsonify(resultado), 200


def obtener_juego_endpoint(juego_id: str):
    """Handler GET /juegos/<id>: devuelve un juego por Q-id (catálogo o Wikidata).

    Args:
        juego_id: Q-id del juego.

    Returns:
        Response: JSON del juego y 200; 404 si no encontrado o falla la API.
    """
    juego = obtener_juego(juego_id)
    if juego is None:
        return jsonify({"error": "juego no encontrado"}), 404
    return jsonify(juego), 200
