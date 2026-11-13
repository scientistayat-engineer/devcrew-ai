"""FastAPI entry point:  uvicorn app.main:app --reload"""
from app.config import settings  # noqa: I001  (must load first: sets CrewAI env defaults)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.observability.langsmith import setup_tracing

TRACING_ENABLED = setup_tracing()

app = FastAPI(title="DevCrew AI", version="1.0.0",
              description="Multi-agent AI software development team (CrewAI + Groq + LangSmith)")
app.add_middleware(CORSMiddleware, allow_origins=list(settings.allowed_origins),
                   allow_methods=["*"], allow_headers=["*"])
app.include_router(router)
