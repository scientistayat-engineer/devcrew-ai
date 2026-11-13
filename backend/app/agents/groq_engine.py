"""Lightweight engine: the same agent roles, called directly through the Groq SDK.

The groq package is tiny, so this engine fits easily inside Vercel's 500 MB Python bundle limit.
"""
from groq import Groq

from app.agents.roles import ROLES
from app.config import resolve_model, settings

# Output token budgets per agent. Groq counts the *requested* output size against the per-minute
# token limit (free tier is small), so modest budgets keep every request inside the limit.
BUDGET = {"coder": 1800, "tester": 1500, "reporter": 3000}
DEFAULT_BUDGET = 900


def run_stage(key: str, ctx: dict, model: str | None = None, temperature: float | None = None) -> str:
    spec = ROLES[key]
    name = resolve_model(model or settings.model)
    extra = {"max_completion_tokens": BUDGET.get(key, DEFAULT_BUDGET)}
    if name.startswith("openai/gpt-oss"):
        extra["reasoning_effort"] = "low"  # fewer hidden reasoning tokens, faster and cheaper
    system = (f"You are a {spec['role']}. Your goal: {spec['goal']} {spec['backstory']} "
              "Be concise and skip long introductions.")
    user = f"{spec['task'].format(**ctx)}\n\nExpected output: {spec['output']}"
    # max_retries lets the SDK wait and retry when Groq answers 429 (per-minute rate limit).
    client = Groq(api_key=settings.groq_api_key, max_retries=5, timeout=120)
    response = client.chat.completions.create(
        model=name,
        temperature=settings.temperature if temperature is None else temperature,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        extra_body=extra,
    )
    return response.choices[0].message.content or ""
