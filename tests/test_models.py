"""Unit tests for Pydantic schemas."""

import pytest
from pydantic import ValidationError

from app.models import CardData, DeckRequest


def test_deck_request_valid():
    req = DeckRequest(cards=["Dark Magician", "Blue-Eyes White Dragon"])
    assert len(req.cards) == 2


def test_deck_request_single_card():
    req = DeckRequest(cards=["Exodia the Forbidden One"])
    assert req.cards[0] == "Exodia the Forbidden One"


def test_deck_request_empty_raises():
    with pytest.raises(ValidationError):
        DeckRequest(cards=[])


def test_deck_request_over_limit_raises():
    with pytest.raises(ValidationError):
        DeckRequest(cards=["Card"] * 61)


def test_card_data_def_alias():
    card = CardData.model_validate({
        "name": "Blue-Eyes White Dragon",
        "type": "Normal Monster",
        "desc": "A legendary dragon.",
        "atk": 3000,
        "def": 2500,
        "level": 8,
        "race": "Dragon",
        "attribute": "LIGHT",
    })
    assert card.def_ == 2500
    assert card.atk == 3000


def test_card_data_optional_fields_default_none():
    card = CardData(name="Pot of Greed", type="Spell Card", desc="Draw 2 cards.")
    assert card.atk is None
    assert card.def_ is None
    assert card.level is None
    assert card.race is None
    assert card.attribute is None


def test_card_data_missing_required_raises():
    with pytest.raises(ValidationError):
        CardData(name="Dark Magician")
