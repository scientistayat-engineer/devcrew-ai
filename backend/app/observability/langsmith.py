"""Enable LangSmith tracing when an API key is present."""
import os


def setup_tracing() -> bool:
    if not os.getenv("LANGSMITH_API_KEY"):
        return False
    os.environ.setdefault("LANGSMITH_TRACING", "true")
    os.environ.setdefault("LANGSMITH_PROJECT", "devcrew-ai")
    return True
