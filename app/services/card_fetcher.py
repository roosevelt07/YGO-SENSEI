"""YGOPRODeck API integration for fetching card data."""

from typing import Optional

import httpx

from app.config import settings
from app.models import CardData


async def fetch_card(name: str) -> Optional[CardData]:
    url = f"{settings.ygoprodeck_base_url}/cardinfo.php"
    async with httpx.AsyncClient(timeout=settings.http_timeout) as client:
        response = await client.get(url, params={"name": name})
        if response.status_code != 200:
            return None
        card = response.json()["data"][0]
        return CardData.model_validate(card)
