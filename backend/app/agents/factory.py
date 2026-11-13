"""Builds CrewAI agents that run on Groq models (imported only when the CrewAI engine is used)."""
from app.agents.roles import ROLES
from app.config import resolve_model, settings


def build_llm(model: str | None = None, temperature: float | None = None):
    """Groq exposes an OpenAI-compatible API, so CrewAI's native OpenAI integration can call it
    directly. This avoids the LiteLLM fallback, which is no longer installed with CrewAI by default."""
    from crewai import LLM

    return LLM(
        model=resolve_model(model or settings.model),
        custom_openai=True,
        base_url=settings.groq_base_url,
        api_key=settings.groq_api_key,
        temperature=settings.temperature if temperature is None else temperature,
    )


def build_agent(key: str, llm):
    from crewai import Agent

    r = ROLES[key]
    return Agent(role=r["role"], goal=r["goal"], backstory=r["backstory"],
                 llm=llm, allow_delegation=False, verbose=False)
