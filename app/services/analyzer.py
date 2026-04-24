"""LLM-powered deck synergy analysis using the Google Generative AI API."""

from typing import List

from google import genai
from google.genai import types

from app.config import settings
from app.models import CardData

_client = genai.Client(api_key=settings.google_api_key)

_SYSTEM_PROMPT = """Você é o Sensei do Duelo — um duelista experiente e estrategista de Yu-Gi-Oh! com décadas de experiência em competições.
Você analisa decks com profundidade técnica e paixão, respondendo sempre em português brasileiro.

Sua análise deve cobrir:
- Estratégia central do deck
- Sinergias entre as cartas
- Pontos fortes e vulnerabilidades
- Sugestões de melhoria (se aplicável)

Seja direto, entusiasmado e use a terminologia do jogo naturalmente."""


def analyze_deck(cards: List[CardData], cards_not_found: List[str]) -> str:
    cards_text = "\n".join(
        f"- {c.name} ({c.type}): {c.desc[:200]}"
        for c in cards
    )

    if cards_not_found:
        cards_text += f"\n\nCartas não encontradas na base: {', '.join(cards_not_found)}"

    response = _client.models.generate_content(
        model=settings.llm_model,
        contents=f"Analise a sinergia estratégica deste deck:\n\n{cards_text}",
        config=types.GenerateContentConfig(
            system_instruction=_SYSTEM_PROMPT,
        ),
    )

    return response.text
