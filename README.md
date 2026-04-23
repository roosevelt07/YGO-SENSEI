# ygo-sensei

> Strategic Yu-Gi-Oh! deck analysis powered by AI

## Overview

**ygo-sensei** is a REST API built with FastAPI that receives a list of Yu-Gi-Oh! card
names, fetches real card data from the [YGOPRODeck API](https://ygoprodeck.com/api-guide/),
and uses an LLM to analyze the deck's strategic synergy — responding like an experienced
duelist in Brazilian Portuguese.

## Architecture

```
ygo-sensei/
├── main.py                        # FastAPI app entry point
├── requirements.txt
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
git clone <repo-url>
cd ygo-sensei

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env and fill in your ANTHROPIC_API_KEY

# 5. Start the API
uvicorn main:app --reload
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | ✅ Yes | — | Anthropic API key |
| `LLM_MODEL` | No | `claude-haiku-4-5-20251001` | Claude model for analysis |
| `YGOPRODECK_BASE_URL` | No | `https://db.ygoprodeck.com/api/v7` | Card database API |
| `HTTP_TIMEOUT` | No | `10` | Outbound request timeout (seconds) |

## Endpoints

> Full documentation available at `http://localhost:8000/docs` after starting the API.

### POST /analyze

_Documentation coming in Etapa 5._

### GET /card/{name}

_Documentation coming in Etapa 5._

### GET /health

_Documentation coming in Etapa 5._

## Limitations & Next Steps

- Currently limited to cards available in the YGOPRODeck database
- LLM analysis quality depends on the selected Claude model
- Rate limits from YGOPRODeck API may apply for large decks
