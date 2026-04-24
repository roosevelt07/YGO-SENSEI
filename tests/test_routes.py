"""Integration tests for all API routes."""

from unittest.mock import AsyncMock, patch


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# --- GET /card/{name} ---

def test_get_card_found(client, dark_magician):
    with patch("app.routers.deck.fetch_card", new=AsyncMock(return_value=dark_magician)):
        response = client.get("/card/Dark Magician")

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Dark Magician"
    assert data["atk"] == 2500


def test_get_card_not_found(client):
    with patch("app.routers.deck.fetch_card", new=AsyncMock(return_value=None)):
        response = client.get("/card/Carta Inexistente")

    assert response.status_code == 404
    assert "Carta Inexistente" in response.json()["detail"]


# --- POST /analyze ---

def test_analyze_all_cards_found(client, dark_magician, blue_eyes):
    cards = [dark_magician, blue_eyes]

    def fake_fetch(name):
        return next((c for c in cards if c.name == name), None)

    with patch("app.routers.deck.fetch_card", new=AsyncMock(side_effect=fake_fetch)), \
         patch("app.routers.deck.analyze_deck", return_value="Deck sólido com grande sinergia!"):
        response = client.post("/analyze", json={"cards": ["Dark Magician", "Blue-Eyes White Dragon"]})

    assert response.status_code == 200
    data = response.json()
    assert data["analysis"] == "Deck sólido com grande sinergia!"
    assert len(data["cards_found"]) == 2
    assert data["cards_not_found"] == []


def test_analyze_partial_not_found(client, dark_magician):
    def fake_fetch(name):
        return dark_magician if name == "Dark Magician" else None

    with patch("app.routers.deck.fetch_card", new=AsyncMock(side_effect=fake_fetch)), \
         patch("app.routers.deck.analyze_deck", return_value="Análise parcial"):
        response = client.post("/analyze", json={"cards": ["Dark Magician", "Carta Fake"]})

    assert response.status_code == 200
    data = response.json()
    assert len(data["cards_found"]) == 1
    assert "Carta Fake" in data["cards_not_found"]


def test_analyze_no_valid_cards_returns_422(client):
    with patch("app.routers.deck.fetch_card", new=AsyncMock(return_value=None)):
        response = client.post("/analyze", json={"cards": ["Carta Inexistente"]})

    assert response.status_code == 422


def test_analyze_empty_list_returns_422(client):
    response = client.post("/analyze", json={"cards": []})
    assert response.status_code == 422
