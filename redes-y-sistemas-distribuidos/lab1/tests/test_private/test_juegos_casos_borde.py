"""
Tests que debés implementar: casos borde de la lista de juegos.
Contrato: POST con juego_id (id del catálogo). Completar según openapi.yaml.
"""

import pytest

from conftest import JUEGO_TEST_ID, client 

JUEGO_ID_INEXISTENTE = "Q99999"
@pytest.fixture
def usuario_id(client):
    r = client.post("/usuarios", json={"nombre": "UsuarioBorde"})
    assert r.status_code == 201
    return r.get_json()["id"]


def test_agregar_juego_falta_campo_obligatorio_400(client, usuario_id):
    # TODO: POST sin un campo obligatorio (ej. juego_id) debe devolver 400
    r = client.get("/juegos?q=zelda&fuente=wikidata")
    assert r.status_code == 200
    body = {
        # "juego_id": JUEGO_ID_INEXISTENTE,
        "tengo": True,
        "quiero": False,
        "jugado": False,
        "me_gusta": False,
    }
    resp = client.post(f"/usuarios/{usuario_id}/juegos", json=body)
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_actualizar_juego_id_inexistente_404(client, usuario_id):
    # TODO: PUT /usuarios/<id>/juegos/Q99999 (no en lista) debe devolver 404
    client.get("/juegos?q=zelda&fuente=wikidata")
    resp = client.put(
        f"/usuarios/{usuario_id}/juegos/{JUEGO_ID_INEXISTENTE}",
        json={"jugado": True, "me_gusta": True},
    )
    assert resp.status_code == 404
    assert "error" in resp.get_json()


def test_eliminar_juego_no_en_lista_404(client, usuario_id):
    # TODO: DELETE /usuarios/<id>/juegos/<juego_id> con juego no en la lista debe devolver 404
    client.get("/juegos?q=zelda&fuente=wikidata")
    client.post(
        f"/usuarios/{usuario_id}/juegos",
        json={
            "juego_id": JUEGO_TEST_ID,
            "tengo": False,
            "quiero": True,
            "jugado": False,
            "me_gusta": False,
        },
    )
    resp = client.delete(f"/usuarios/{usuario_id}/juegos/{JUEGO_ID_INEXISTENTE}")
    assert resp.status_code == 404
    assert "error" in resp.get_json()

def test_agregar_juego_id_inexistente_404(client, usuario_id):
    # TODO: POST con juego_id que no existe en catálogo ni Wikidata debe devolver 404
    r = client.get("/juegos?q=zelda&fuente=wikidata")
    assert r.status_code == 200
    body = {
        "juego_id": JUEGO_ID_INEXISTENTE,
        "tengo": True,
        "quiero": False,
        "jugado": False,
        "me_gusta": False,
    }
    resp = client.post(f"/usuarios/{usuario_id}/juegos", json=body)
    assert resp.status_code == 404
    assert "error" in resp.get_json()


def test_ordenar_por_fecha_lanzamiento(client, usuario_id):
   juegos = [
    {"id": "Q1", "fecha_lanzamiento": "2020-02-01"},
    {"id": "Q2", "fecha_lanzamiento": "2018-04-13"},
    {"id": "Q3", "fecha_lanzamiento": "2022-02-27"},
    {"id": "Q4", "fecha_lanzamiento": "2015-05-07"},
    {"id": "Q5", "fecha_lanzamiento": "2022-09-15"},
    ]   
   resp = client.get(f"/usuarios/{usuario_id}/juegos?ordenar=fecha_lanzamiento&orden=asc")
   assert resp.status_code == 200
   data = resp.get_json()
   assert isinstance(data, list)
   fechas = [item.get("fecha_lanzamiento") for item in data]
   assert fechas == sorted(fechas)

