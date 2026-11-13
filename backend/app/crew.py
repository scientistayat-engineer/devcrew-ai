"""Pipeline orchestration: every agent runs as its own stage and its own LangSmith trace.

Two interchangeable engines run the same agent roles (see agents/roles.py):
  * crewai : CrewAI Agent + Task + Crew per stage (full CrewAI, larger install)
  * groq   : direct Groq SDK calls (tiny install, fits Vercel's 500 MB Python bundle limit)
AGENT_ENGINE=auto (default) uses CrewAI when crewai and its openai extra are installed, else the Groq engine.
"""
import importlib.util
import time

from langsmith import traceable

from app.agents.roles import PIPELINE, ROLES
from app.config import settings
from app.schemas import StageResult
from app.utils import extract_code


def _stage_crewai(key: str, model, temperature, ctx: dict) -> str:
    from crewai import Crew, Process, Task

    from app.agents.factory import build_agent, build_llm

    spec = ROLES[key]
    agent = build_agent(key, build_llm(model, temperature))
    task = Task(description=spec["task"].format(**ctx), expected_output=spec["output"], agent=agent)
    return Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff().raw


def _stage_groq(key: str, model, temperature, ctx: dict) -> str:
    from app.agents.groq_engine import run_stage

    return run_stage(key, ctx, model, temperature)


# Keep prompts small: long earlier outputs are clipped before they are sent to the next agent.
LIMITS = {"requirement": 2000, "analysis": 1500, "plan": 1500, "code": 4000, "tests": 2500, "review": 1500, "security": 1200}


def _clip(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[:limit] + "\n...[truncated to save tokens]"


def _prompt_ctx(ctx: dict) -> dict:
    return {k: _clip(v, LIMITS.get(k, 2000)) for k, v in ctx.items()}


ENGINES = {"crewai": _stage_crewai, "groq": _stage_groq}


def pick_engine(name: str | None = None) -> str:
    name = (name or "auto").lower()
    if name == "auto":
        ready = all(importlib.util.find_spec(m) for m in ("crewai", "openai"))
        return "crewai" if ready else "groq"
    if name not in ENGINES:
        raise ValueError(f"Unknown AGENT_ENGINE '{name}'. Use auto, crewai or groq.")
    return name


@traceable(name="devcrew_pipeline", run_type="chain")
def run_pipeline(requirement: str, model: str | None = None, temperature: float | None = None) -> dict:
    stage = ENGINES[pick_engine(settings.engine)]
    ctx: dict = {"requirement": requirement}
    stages: list[StageResult] = []
    for key in PIPELINE:
        start = time.perf_counter()
        output = traceable(name=f"agent:{key}", run_type="chain")(stage)(key, model, temperature, _prompt_ctx(ctx))
        ctx[ROLES[key]["store_as"]] = output
        stages.append(StageResult(agent=ROLES[key]["role"], output=output,
                                  seconds=round(time.perf_counter() - start, 2)))
    final_code = extract_code(ctx["report"]) or extract_code(ctx["code"])
    return {"stages": stages, "final_code": final_code, "report": ctx["report"]}
