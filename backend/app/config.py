"""Central configuration loaded from environment variables (.env)."""
import os
import tempfile
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

# CrewAI writes small files. Serverless hosts (Vercel) only allow writing to the temp dir,
# so point the user-data folder there when running on Vercel (not needed locally).
if os.getenv("VERCEL"):
    os.environ.setdefault("XDG_DATA_HOME", tempfile.gettempdir())
os.environ.setdefault("CREWAI_DISABLE_TELEMETRY", "true")
os.environ.setdefault("OTEL_SDK_DISABLED", "true")


@dataclass(frozen=True)
class Settings:
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    model: str = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    engine: str = os.getenv("AGENT_ENGINE", "auto")  # auto | crewai | groq
    groq_base_url: str = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
    temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.3"))
    require_auth: bool = os.getenv("REQUIRE_AUTH", "false").lower() == "true"
    firebase_project_id: str = os.getenv("FIREBASE_PROJECT_ID", "")
    allowed_origins: tuple = tuple(
        o.strip() for o in os.getenv("ALLOWED_ORIGINS", "http://localhost:5500,http://localhost:3000").split(",") if o.strip()
    )


# Groq retired these model IDs (16 Aug 2026); map them to the recommended replacements.
MODEL_ALIASES = {"llama-3.3-70b-versatile": "openai/gpt-oss-120b", "llama-3.1-8b-instant": "openai/gpt-oss-20b"}


def resolve_model(name: str) -> str:
    return MODEL_ALIASES.get(name, name)


settings = Settings()
