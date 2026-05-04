"""Tests públicos: endpoints de autenticación básica (registro, login y uso de token)."""

import datetime as dt

from src import store


def _auth_headers(token: str) -> dict[str, str]:
    """Helper: arma el header Authorization: Token <TOKEN>."""
    return {"Authorization": f"Token {token}"}


def test_registro_crea_usuario_y_hash(client):
    """POST /auth/registro crea usuario y guarda password_hash (no texto plano)."""
    body = {"username": "alice", "nombre": "Alice", "password": "secreta"}
    r = client.post("/auth/registro", json=body)
    assert r.status_code == 201
    usuario = r.get_json()
    assert usuario["nombre"] == "Alice"
    cred = store.obtener_credenciales_por_username("alice")
    assert cred is not None
    assert cred["password_hash"] != "secreta"


def test_login_devuelve_token(client):
    """POST /auth/login con credenciales válidas devuelve un token opaco."""
    client.post("/auth/registro", json={"username": "bob", "nombre": "Bob", "password": "clave"})
    r = client.post("/auth/login", json={"username": "bob", "password": "clave"})
    assert r.status_code == 200
    data = r.get_json()
    assert "token" in data and isinstance(data["token"], str) and data["token"]


def test_token_permite_acceder_a_su_lista(client, wikidata_mock):
    """Un token válido permite agregar y leer juegos de la propia lista."""
    r = client.post("/auth/registro", json={"username": "carol", "nombre": "Carol", "password": "clave"})
    usuario_id = r.get_json()["id"]
    r_login = client.post("/auth/login", json={"username": "carol", "password": "clave"})
    token = r_login.get_json()["token"]

    body = {
        "juego_id": "Q12395",
        "tengo": True,
        "quiero": False,
        "jugado": False,
        "me_gusta": False,
    }
    r_add = client.post(f"/usuarios/{usuario_id}/juegos", json=body, headers=_auth_headers(token))
    assert r_add.status_code == 201

    r_lista = client.get(f"/usuarios/{usuario_id}/juegos", headers=_auth_headers(token))
    assert r_lista.status_code == 200
    items = r_lista.get_json()
    assert any(it["id"] == "Q12395" for it in items)


def test_token_expirado_rechazado_401(client):
    """Un token expirado es rechazado con 401 al acceder a un endpoint protegido."""
    r = client.post("/auth/registro", json={"username": "dave", "nombre": "Dave", "password": "clave"})
    usuario_id = r.get_json()["id"]
    r_login = client.post("/auth/login", json={"username": "dave", "password": "clave"})
    token = r_login.get_json()["token"]

    vencido = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=5)).isoformat().replace("+00:00", "Z")
    cred = store.obtener_credenciales_por_username("dave")
    store.actualizar_token(cred["usuario_id"], token, vencido)

    body = {
        "juego_id": "Q12395",
        "tengo": True,
        "quiero": False,
        "jugado": False,
        "me_gusta": False,
    }
    r_add = client.post(f"/usuarios/{usuario_id}/juegos", json=body, headers=_auth_headers(token))
    assert r_add.status_code == 401


def test_no_puedo_modificar_otro_usuario(client):
    """Un usuario autenticado no puede modificar datos de otro usuario (401)."""
    r1 = client.post("/auth/registro", json={"username": "eva", "nombre": "Eva", "password": "clave"})
    r1.get_json()["id"]
    r2 = client.post("/auth/registro", json={"username": "fran", "nombre": "Fran", "password": "clave"})
    user_b = r2.get_json()["id"]

    r_login = client.post("/auth/login", json={"username": "eva", "password": "clave"})
    token_a = r_login.get_json()["token"]

    r_put = client.put(
        f"/usuarios/{user_b}",
        json={"nombre": "Otro"},
        headers=_auth_headers(token_a),
    )
    assert r_put.status_code == 401

