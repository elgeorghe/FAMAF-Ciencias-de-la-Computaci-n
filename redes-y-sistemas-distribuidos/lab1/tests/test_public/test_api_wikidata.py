"""Tests públicos: GET /health, GET /juegos (listar catálogo, búsqueda local, búsqueda Wikidata)."""

import requests_mock

from src.store import CATALOGO_JUEGOS


def test_health_ok(client):
    """GET /health devuelve 200 y { status: ok }."""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_listar_juegos_devuelve_catalogo(client):
    """GET /juegos devuelve 200 y lista (catálogo local); vacía si no se buscó nada."""
    resp = client.get("/juegos")
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)


def test_juegos_fuente_wikidata_fallo_502(client):
    """GET /juegos?q=x&fuente=wikidata cuando Wikidata no responde devuelve 502."""
    with requests_mock.Mocker() as m:
        m.get(
            "https://www.wikidata.org/w/api.php",
            status_code=500,
        )
        resp = client.get("/juegos?q=zelda&fuente=wikidata")
        assert resp.status_code == 502


def test_juegos_fuente_wikidata_puebla_catalogo(client, wikidata_mock):
    """GET /juegos?q=X&fuente=wikidata con mock devuelve 200, puebla catálogo; GET /juegos lo muestra."""
    resp = client.get("/juegos?q=zelda&fuente=wikidata")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    if data:
        assert data[0]["nombre"] == "Zelda"
        assert "descripcion" in data[0]
    cat = client.get("/juegos")
    assert cat.status_code == 200
    catalog_list = cat.get_json()
    assert any(j.get("nombre") == "Zelda" for j in catalog_list)


def test_juegos_busqueda_local(client, wikidata_mock):
    """GET /juegos?q=X (o fuente=local) filtra el catálogo por nombre (case-insensitive)."""
    client.get("/juegos?q=zelda&fuente=wikidata")
    resp = client.get("/juegos?q=zelda")
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) >= 1
    assert data[0]["nombre"] == "Zelda"
    resp2 = client.get("/juegos?q=zelda&fuente=local")
    assert resp2.status_code == 200
    data2 = resp2.get_json()
    assert len(data2) >= 1
    assert data2[0]["nombre"] == "Zelda"


def test_obtener_juego_por_id(client, wikidata_mock):
    """GET /juegos/{id} con mock devuelve 200 y juego (desde Wikidata si no estaba en catálogo)."""
    juego_id = "Q9999"
    resp = client.get(f"/juegos/{juego_id}")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["id"] == juego_id
    assert data["nombre"] == "The Legend of Zelda"


def test_juegos_filtro_genero_orden_desc(client, wikidata_mock):
    """GET /juegos con genero, ordenar y orden=desc devuelve 200, filtrado y ordenado descendente."""
    client.get("/juegos?q=zelda&fuente=wikidata")
    resp = client.get("/juegos?genero=Aventura&ordenar=nombre&orden=desc")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    for item in data:
        assert item.get("genero") == "Aventura"
    nombres = [item.get("nombre") or "" for item in data]
    assert nombres == sorted(nombres, reverse=True, key=str.lower)


def test_obtener_juego_por_id_404(client):
    """GET /juegos/{id} con id inexistente en Wikidata devuelve 404."""
    with requests_mock.Mocker() as m:
        # Wikidata devuelve "missing" para entidad inexistente
        m.get(
            "https://www.wikidata.org/w/api.php",
            json={"entities": {"QNOEXISTE": {"id": "QNOEXISTE", "missing": ""}}},
        )
        resp = client.get("/juegos/QNOEXISTE")
        assert resp.status_code == 404


def test_juegos_ordenar_por_lanzamiento(client):
    """GET /juegos con ordenar=lanzamiento devuelve ordenado por esa fecha."""
    for jid, nombre, fecha in [("Q21", "B", "2022-01-01"), ("Q22", "A", "2020-06-15"), ("Q23", "C", "2023-12-01")]:
        CATALOGO_JUEGOS[jid] = {
            "id": jid,
            "nombre": nombre,
            "genero": "RPG",
            "lanzamiento": fecha,
            "plataforma": "PC",
            "descripcion": "",
        }
    try:
        resp = client.get("/juegos?ordenar=lanzamiento")
        assert resp.status_code == 200
        items = [i for i in resp.get_json() if i["id"] in {"Q21", "Q22", "Q23"}]
        fechas = [i["lanzamiento"] for i in items]
        assert fechas == sorted(fechas)
        resp_desc = client.get("/juegos?ordenar=lanzamiento&orden=desc")
        assert resp_desc.status_code == 200
        items_desc = [i for i in resp_desc.get_json() if i["id"] in {"Q21", "Q22", "Q23"}]
        fechas_desc = [i["lanzamiento"] for i in items_desc]
        assert fechas_desc == sorted(fechas_desc, reverse=True)
    finally:
        for jid in ("Q21", "Q22", "Q23"):
            CATALOGO_JUEGOS.pop(jid, None)


def test_juegos_ordenar_por_genero(client):
    """GET /juegos con ordenar=genero devuelve ordenado por género."""
    for jid, nombre, genero in [("Q31", "JuegoA", "Estrategia"), ("Q32", "JuegoB", "Aventura"), ("Q33", "JuegoC", "RPG")]:
        CATALOGO_JUEGOS[jid] = {
            "id": jid,
            "nombre": nombre,
            "genero": genero,
            "lanzamiento": "2021-01-01",
            "plataforma": "PC",
            "descripcion": "",
        }
    try:
        resp = client.get("/juegos?ordenar=genero")
        assert resp.status_code == 200
        items = [i for i in resp.get_json() if i["id"] in {"Q31", "Q32", "Q33"}]
        generos = [i["genero"] for i in items]
        assert generos == sorted(generos)
    finally:
        for jid in ("Q31", "Q32", "Q33"):
            CATALOGO_JUEGOS.pop(jid, None)


def test_juegos_ordenar_por_id(client):
    """GET /juegos con ordenar=id devuelve ordenado por id."""
    for jid, nombre in [("Q200", "JuegoX"), ("Q150", "JuegoY"), ("Q300", "JuegoZ")]:
        CATALOGO_JUEGOS[jid] = {
            "id": jid,
            "nombre": nombre,
            "genero": "Acción",
            "lanzamiento": "2020-01-01",
            "plataforma": "PC",
            "descripcion": "",
        }
    try:
        resp = client.get("/juegos?ordenar=id")
        assert resp.status_code == 200
        items = [i for i in resp.get_json() if i["id"] in {"Q200", "Q150", "Q300"}]
        ids = [i["id"] for i in items]
        assert ids == sorted(ids)
    finally:
        for jid in ("Q200", "Q150", "Q300"):
            CATALOGO_JUEGOS.pop(jid, None)


def test_obtener_juego_por_id_fallo_wikidata_404(client):
    """GET /juegos/{id} cuando Wikidata falla devuelve 404 (no se pudo obtener el juego)."""
    with requests_mock.Mocker() as m:
        m.get(
            "https://www.wikidata.org/w/api.php",
            status_code=500,
        )
        resp = client.get("/juegos/QERROR")
        assert resp.status_code == 404
