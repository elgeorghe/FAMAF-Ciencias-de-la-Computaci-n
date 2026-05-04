"""Tests públicos: endpoint de sugerencia (random entre juegos que tengo)."""


from conftest import JUEGO_TEST_ID


def test_sugerencia_devuelve_nombre_y_descripcion(client, rawg_mock):
    """GET /usuarios/<id>/sugerencia devuelve 200 con nombre y descripcion."""
    r = client.post("/usuarios", json={"nombre": "Sug"})
    uid = r.get_json()["id"]
    client.get("/juegos?q=zelda&fuente=wikidata")
    client.post(
        f"/usuarios/{uid}/juegos",
        json={
            "juego_id": JUEGO_TEST_ID,
            "tengo": True,
            "quiero": False,
            "jugado": False,
            "me_gusta": False,
        },
    )
    resp = client.get(f"/usuarios/{uid}/sugerencia")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "nombre" in data
    assert "descripcion" in data


def test_sugerencia_404_sin_juegos_que_tenga(client):
    """GET /usuarios/<id>/sugerencia sin juegos con tengo=true devuelve 404."""
    r = client.post("/usuarios", json={"nombre": "Empty"})
    uid = r.get_json()["id"]
    resp = client.get(f"/usuarios/{uid}/sugerencia")
    assert resp.status_code == 404


def test_sugerencia_usuario_inexistente_404(client):
    """GET /usuarios/<id>/sugerencia con usuario inexistente devuelve 404."""
    resp = client.get("/usuarios/99999/sugerencia")
    assert resp.status_code == 404
