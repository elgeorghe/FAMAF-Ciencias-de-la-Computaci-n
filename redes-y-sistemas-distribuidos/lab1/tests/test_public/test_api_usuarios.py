"""Tests públicos: endpoints de usuarios (contrato API)."""



def test_listar_usuarios_vacio_o_con_datos(client):
    """GET /usuarios devuelve 200 y lista (puede estar vacía)."""
    resp = client.get("/usuarios")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)


def test_crear_usuario(client):
    """POST /usuarios con nombre devuelve 201 y usuario con id y nombre."""
    resp = client.post("/usuarios", json={"nombre": "Ana"})
    assert resp.status_code == 201
    data = resp.get_json()
    assert "id" in data
    assert data["nombre"] == "Ana"


def test_crear_usuario_sin_nombre_400(client):
    """POST /usuarios sin nombre devuelve 400."""
    resp = client.post("/usuarios", json={})
    assert resp.status_code == 400


def test_obtener_usuario(client):
    """GET /usuarios/<id> devuelve 200 y usuario si existe."""
    r = client.post("/usuarios", json={"nombre": "Bob"})
    assert r.status_code == 201
    uid = r.get_json()["id"]
    resp = client.get(f"/usuarios/{uid}")
    assert resp.status_code == 200
    assert resp.get_json()["nombre"] == "Bob"


def test_obtener_usuario_404(client):
    """GET /usuarios/<id> inexistente devuelve 404."""
    resp = client.get("/usuarios/99999")
    assert resp.status_code == 404


def test_actualizar_usuario_404(client):
    """PUT /usuarios/<id> inexistente devuelve 404."""
    resp = client.put("/usuarios/99999", json={"nombre": "X"})
    assert resp.status_code == 404


def test_actualizar_usuario_body_invalido_400(client):
    """PUT /usuarios/<id> con body inválido devuelve 400."""
    r = client.post("/usuarios", json={"nombre": "Eve"})
    assert r.status_code == 201
    uid = r.get_json()["id"]
    resp = client.put(f"/usuarios/{uid}", json={})
    assert resp.status_code == 400


def test_eliminar_usuario_404(client):
    """DELETE /usuarios/<id> inexistente devuelve 404."""
    resp = client.delete("/usuarios/99999")
    assert resp.status_code == 404


def test_actualizar_usuario(client):
    """PUT /usuarios/<id> actualiza nombre."""
    r = client.post("/usuarios", json={"nombre": "Carlos"})
    uid = r.get_json()["id"]
    resp = client.put(f"/usuarios/{uid}", json={"nombre": "Carlos M."})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["nombre"] == "Carlos M."


def test_eliminar_usuario(client):
    """DELETE /usuarios/<id> devuelve 200 y mensaje."""
    r = client.post("/usuarios", json={"nombre": "Diana"})
    uid = r.get_json()["id"]
    resp = client.delete(f"/usuarios/{uid}")
    assert resp.status_code == 200
    assert "mensaje" in resp.get_json()
    assert client.get(f"/usuarios/{uid}").status_code == 404
