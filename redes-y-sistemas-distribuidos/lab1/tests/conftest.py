"""Pytest fixtures: cliente Flask para tests."""

import os
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# Usar SQLite en memoria para tests (antes de importar la app/store)
os.environ.setdefault("LAB1_DATABASE", ":memory:")

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

import pytest # noqa: E402
import requests_mock # noqa: E402
from src.app import app  # noqa: E402

# Id y datos de juego de prueba para tests que usan catálogo (Wikidata mock)
JUEGO_TEST_ID = "Q12395"

# Respuestas mock para la API de Wikidata
WIKIDATA_SEARCH_RESPONSE = {
    "search": [
        {"id": JUEGO_TEST_ID, "label": "Zelda", "description": "video game"},
    ]
}

WIKIDATA_ENTITIES_CLAIMS = {
    "entities": {
        JUEGO_TEST_ID: {
            "id": JUEGO_TEST_ID,
            "claims": {
                "P31": [{"mainsnak": {"datavalue": {"value": {"id": "Q7889"}}}}],
                "P577": [{"mainsnak": {"datavalue": {"value": {"time": "+1986-02-21T00:00:00Z"}}}}],
                "P136": [{"mainsnak": {"datavalue": {"value": {"id": "Q343568"}}}}],
                "P400": [{"mainsnak": {"datavalue": {"value": {"id": "Q188642"}}}}],
            },
        }
    }
}

WIKIDATA_ENTITIES_FULL = {
    "entities": {
        JUEGO_TEST_ID: {
            "id": JUEGO_TEST_ID,
            "labels": {"es": {"value": "Zelda"}, "en": {"value": "Zelda"}},
            "descriptions": {"es": {"value": "Un juego"}, "en": {"value": "A game"}},
            "claims": {
                "P31": [{"mainsnak": {"datavalue": {"value": {"id": "Q7889"}}}}],
                "P577": [{"mainsnak": {"datavalue": {"value": {"time": "+1986-02-21T00:00:00Z"}}}}],
                "P136": [{"mainsnak": {"datavalue": {"value": {"id": "Q343568"}}}}],
                "P400": [{"mainsnak": {"datavalue": {"value": {"id": "Q188642"}}}}],
            },
        }
    }
}

WIKIDATA_LABELS_GENRE_PLATFORM = {
    "entities": {
        "Q343568": {"labels": {"es": {"value": "Aventura"}}},
        "Q188642": {"labels": {"es": {"value": "Switch"}}},
    }
}


def _entity_for_id(qid: str):
    """Entidad completa para un Q-id (para GET por id)."""
    return {
        "entities": {
            qid: {
                "id": qid,
                "labels": {"es": {"value": "The Legend of Zelda"}, "en": {"value": "The Legend of Zelda"}},
                "descriptions": {"es": {"value": "Un clásico"}, "en": {"value": "A classic"}},
                "claims": {
                    "P31": [{"mainsnak": {"datavalue": {"value": {"id": "Q7889"}}}}],
                    "P577": [{"mainsnak": {"datavalue": {"value": {"time": "+2017-03-03T00:00:00Z"}}}}],
                    "P136": [{"mainsnak": {"datavalue": {"value": {"id": "Q343568"}}}}],
                    "P400": [{"mainsnak": {"datavalue": {"value": {"id": "Q188642"}}}}],
                },
            }
        }
    }


def _wikidata_matcher(request):
    """Devuelve el JSON según action y props del request a api.php."""
    parsed = urlparse(request.url)
    if "wikidata.org" not in parsed.netloc or "/w/api.php" not in parsed.path:
        return None
    qs = parse_qs(parsed.query)
    action = (qs.get("action") or [""])[0]
    props = (qs.get("props") or [""])[0]
    ids_param = (qs.get("ids") or [""])[0]
    id_list = [x.strip() for x in ids_param.split("|")] if ids_param else []
    if action == "wbsearchentities":
        return WIKIDATA_SEARCH_RESPONSE
    if action == "wbgetentities":
        if props == "claims":
            return WIKIDATA_ENTITIES_CLAIMS
        if "labels" in props and "descriptions" in props and "claims" in props:
            if JUEGO_TEST_ID in id_list or ids_param == JUEGO_TEST_ID:
                return WIKIDATA_ENTITIES_FULL
            # Llamada por un solo id (ej. obtener_juego Q9999)
            if len(id_list) == 1:
                return _entity_for_id(id_list[0])
            return {"entities": {}}
        if props == "labels":
            return WIKIDATA_LABELS_GENRE_PLATFORM
    return None


@pytest.fixture
def client():
    """Cliente de prueba Flask."""
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


@pytest.fixture
def wikidata_mock():
    """Mock de Wikidata: búsqueda y GET por id devuelven JUEGO_TEST_ID."""
    with requests_mock.Mocker() as m:
        def callback(request, context):
            result = _wikidata_matcher(request)
            return result if result is not None else {}

        m.get(
            "https://www.wikidata.org/w/api.php",
            json=callback,
            additional_matcher=lambda req: "wikidata.org" in (req.url or ""),
        )
        yield m


# Alias para compatibilidad con tests que usan el nombre rawg_mock
@pytest.fixture
def rawg_mock(wikidata_mock):
    """Alias de wikidata_mock para compatibilidad con tests que referencian rawg_mock."""
    return wikidata_mock
