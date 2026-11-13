"""Small helpers."""
import re

_FENCE = re.compile(r"```(?:python|py)?[ \t]*\n(.*?)(?:```|\Z)", re.S)


def extract_code(text: str) -> str:
    """Return the longest fenced code block from an LLM answer (also when the last fence is missing)."""
    blocks = _FENCE.findall(text or "")
    return max(blocks, key=len).strip() if blocks else ""
