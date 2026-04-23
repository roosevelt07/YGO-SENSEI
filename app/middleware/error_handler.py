"""Global exception handler for unexpected runtime errors."""

import httpx
from fastapi import Request
from fastapi.responses import JSONResponse


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, httpx.TimeoutException):
        return JSONResponse(
            status_code=504,
            content={"detail": "Timeout ao consultar a API de cartas."},
        )
    if isinstance(exc, httpx.HTTPError):
        return JSONResponse(
            status_code=502,
            content={"detail": "Erro ao consultar a API de cartas."},
        )
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor."},
    )
