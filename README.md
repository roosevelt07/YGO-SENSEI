# ygo-sensei

> Strategic Yu-Gi-Oh! deck analysis powered by AI

## Overview

**ygo-sensei** is a REST API built with FastAPI that receives a list of Yu-Gi-Oh! card
names, fetches real card data from the [YGOPRODeck API](https://ygoprodeck.com/api-guide/),
and uses Google Gemini to analyze the deck's strategic synergy — responding like an experienced
duelist in Brazilian Portuguese.

## Architecture

```
ygo-sensei/
├── main.py                        # FastAPI app entry point
├── requirements.txt
├── requirements-dev.txt           # Dev/test dependencies
├── .env.example
└── app/
    ├── config.py                  # Environment settings (Pydantic Settings)
    ├── models.py                  # Pydantic request/response schemas
    ├── routers/
    │   └── deck.py                # API route handlers
    ├── services/
    │   ├── card_fetcher.py        # YGOPRODeck API integration
    │   └── analyzer.py            # LLM synergy analysis
    └── middleware/
        └── error_handler.py       # Global exception handling
```

## Setup

```bash
# 1. Clone and enter the project
git clone https://github.com/roosevelt07/YGO-SENSEI.git
cd YGO-SENSEI

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env and fill in your GEMINI_API_KEY

# 5. Start the API
uvicorn main:app --reload
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | ✅ Yes | — | Google Gemini API key ([get yours here](https://aistudio.google.com/app/apikey)) |
| `LLM_MODEL` | No | `gemini-1.5-flash` | Gemini model used for analysis |
| `YGOPRODECK_BASE_URL` | No | `https://db.ygoprodeck.com/api/v7` | Card database API base URL |
| `HTTP_TIMEOUT` | No | `10` | Outbound request timeout in seconds |

## Endpoints

> Full interactive documentation available at `http://localhost:8000/docs` after starting the API.

### GET /health

Returns the API status.

**Response**
```json
{ "status": "ok" }
```

---

### GET /card/{name}

Fetches data for a single card from the YGOPRODeck database.

**Path parameter:** `name` — exact card name (e.g. `Dark Magician`)

**Response 200**
```json
{
  "name": "Dark Magician",
  "type": "Normal Monster",
  "desc": "The ultimate wizard in terms of attack and defense.",
  "atk": 2500,
  "def": 2100,
  "level": 7,
  "race": "Spellcaster",
  "attribute": "DARK"
}
```

**Response 404** — card not found.

---

### POST /analyze

Receives a list of card names, fetches their data, and returns an AI-generated strategic analysis of the deck's synergy in Brazilian Portuguese.

**Request body**
```json
{
  "cards": ["Dark Magician", "Dark Magician Girl", "Mystic Box"]
}
```

- `cards`: list of card names — minimum 1, maximum 60.

**Response 200**
```json
{
  "analysis": "Este deck gira em torno do Dark Magician como peça central...",
  "cards_found": [ { "name": "Dark Magician", "type": "Normal Monster", ... } ],
  "cards_not_found": []
}
```

**Response 422** — no valid cards found or empty list.

## Running Tests

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

## Limitations

- Card lookup is limited to cards available in the YGOPRODeck database
- Analysis quality depends on the selected Gemini model
- YGOPRODeck API may apply rate limits for large decks
