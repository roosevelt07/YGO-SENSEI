"""Pydantic schemas for request and response payloads."""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DeckRequest(BaseModel):
    cards: List[str] = Field(..., min_length=1, max_length=60)


class CardData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    type: str
    desc: str
    atk: Optional[int] = None
    def_: Optional[int] = Field(None, alias="def")
    level: Optional[int] = None
    race: Optional[str] = None
    attribute: Optional[str] = None


class DeckAnalysisResponse(BaseModel):
    analysis: str
    cards_found: List[CardData]
    cards_not_found: List[str]
