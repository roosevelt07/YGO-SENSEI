"""API route handlers for deck analysis and card lookup."""

from typing import List

from fastapi import APIRouter, HTTPException

from app.models import CardData, DeckAnalysisResponse, DeckRequest
from app.services.analyzer import analyze_deck
from app.services.card_fetcher import fetch_card

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/card/{name}", response_model=CardData)
async def get_card(name: str):
    card = await fetch_card(name)
    if not card:
        raise HTTPException(status_code=404, detail=f"Carta '{name}' não encontrada.")
    return card


@router.post("/analyze", response_model=DeckAnalysisResponse)
async def analyze(request: DeckRequest):
    cards_found: List[CardData] = []
    cards_not_found: List[str] = []

    for name in request.cards:
        card = await fetch_card(name)
        if card:
            cards_found.append(card)
        else:
            cards_not_found.append(name)

    if not cards_found:
        raise HTTPException(
            status_code=422,
            detail="Nenhuma carta válida encontrada. Verifique os nomes e tente novamente.",
        )

    analysis = analyze_deck(cards_found, cards_not_found)

    return DeckAnalysisResponse(
        analysis=analysis,
        cards_found=cards_found,
        cards_not_found=cards_not_found,
    )
