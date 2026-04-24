"""Shared fixtures for the test suite."""

import pytest
from fastapi.testclient import TestClient

from app.models import CardData
from main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def dark_magician():
    return CardData.model_validate({
        "name": "Dark Magician",
        "type": "Normal Monster",
        "desc": "The ultimate wizard in terms of attack and defense.",
        "atk": 2500,
        "def": 2100,
        "level": 7,
        "race": "Spellcaster",
        "attribute": "DARK",
    })


@pytest.fixture
def blue_eyes():
    return CardData.model_validate({
        "name": "Blue-Eyes White Dragon",
        "type": "Normal Monster",
        "desc": "A legendary dragon that is the stuff of myths.",
        "atk": 3000,
        "def": 2500,
        "level": 8,
        "race": "Dragon",
        "attribute": "LIGHT",
    })
