"""FastAPI application entry point."""

from fastapi import FastAPI

from app.middleware.error_handler import global_exception_handler
from app.routers.deck import router

app = FastAPI(
    title="ygo-sensei",
    description="Strategic Yu-Gi-Oh! deck analysis powered by AI",
    version="0.1.0",
)

app.add_exception_handler(Exception, global_exception_handler)
app.include_router(router)
