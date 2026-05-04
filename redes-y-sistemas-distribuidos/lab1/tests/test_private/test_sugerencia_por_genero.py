"""
Tests que debés implementar: sugerencia con filtro por género.
Completar los tests según el contrato de la API.
"""

import pytest
from conftest import JUEGO_TEST_ID


def test_sugerencia_con_genero_solo_devuelve_ese_genero(client):
    """Sugerencia con ?genero=X solo debe devolver juegos de ese género."""
    # Crear usuario
    r = client.post("/auth/registro", json={"username": "marco", "nombre": "Marco", "password": "clave"})
    assert r.status_code == 201
    usuario_id = r.get_json()["id"]
    
    # Agregar juegos a la lista del usuario
    juego1 = {
        "juego_id": "Q12395",
        "tengo": True,
        "quiero": False,
        "jugado": False,
        "me_gusta": False,
    }
    r_agregar = client.post(f"/usuarios/{usuario_id}/juegos", json=juego1)
    assert r_agregar.status_code == 201
    
    juego2 = {
        "juego_id": "Q189784",
        "tengo": True,
        "quiero": False,
        "jugado": True,
        "me_gusta": True,
    }
    r_agregar2 = client.post(f"/usuarios/{usuario_id}/juegos", json=juego2)
    assert r_agregar2.status_code == 201
    
    # Obtener la lista de juegos para extraer un género válido
    r_lista = client.get(f"/usuarios/{usuario_id}/juegos")
    assert r_lista.status_code == 200
    juegos = r_lista.get_json()
    assert len(juegos) >= 1
    genero_valido = juegos[0]["genero"]
    assert genero_valido, "El juego debe tener un género"
    
    # Solicitar sugerencia con filtro de género
    r_sugerencia = client.get(f"/usuarios/{usuario_id}/sugerencia?genero={genero_valido}")
    assert r_sugerencia.status_code == 200
    
    # Verificar que la sugerencia tiene el género correcto
    juego_sugerido = r_sugerencia.get_json()
    assert "genero" in juego_sugerido
    assert juego_sugerido["genero"] == genero_valido
    
def test_sugerencia_genero_sin_coincidencias_404(client):
    """Sin juegos del género pedido debe devolver 404."""
    # Crear usuario
    r = client.post("/auth/registro", json={"username": "juan", "nombre": "Juan", "password": "clave"})
    assert r.status_code == 201
    usuario_id = r.get_json()["id"]
    
    # Agregar juegos a la lista del usuario
    juego1 = {
        "juego_id": "Q12395",
        "tengo": True,
        "quiero": False,
        "jugado": False,
        "me_gusta": False,
    }
    r_agregar = client.post(f"/usuarios/{usuario_id}/juegos", json=juego1)
    assert r_agregar.status_code == 201
    
    juego2 = {
        "juego_id": "Q189784",
        "tengo": True,
        "quiero": False,
        "jugado": True,
        "me_gusta": True,
    }
    r_agregar2 = client.post(f"/usuarios/{usuario_id}/juegos", json=juego2)
    assert r_agregar2.status_code == 201
    
    # Obtener géneros reales de los juegos
    r_lista = client.get(f"/usuarios/{usuario_id}/juegos")
    assert r_lista.status_code == 200
    juegos = r_lista.get_json()
    generos_existentes = {juego["genero"] for juego in juegos if juego.get("genero")}
    
    # Solicitar sugerencia con un género que NO existe en la lista
    genero_inexistente = "FictionalGenreXYZ"
    r_sugerencia = client.get(f"/usuarios/{usuario_id}/sugerencia?genero={genero_inexistente}")
    assert r_sugerencia.status_code == 404
    assert "No hay juegos que cumplan el criterio" in r_sugerencia.get_json().get("error", "")
