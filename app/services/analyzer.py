"""LLM-powered deck synergy analysis using the Anthropic API."""

from typing import List

import anthropic

from app.config import settings
from app.models import CardData

_client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

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

    response = _client.messages.create(
        model=settings.llm_model,
        max_tokens=1024,
        system=[
            {
                "type": "text",
                "text": _SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[
            {
                "role": "user",
                "content": f"Analise a sinergia estratégica deste deck:\n\n{cards_text}",
            }
        ],
    )

    return response.content[0].text
