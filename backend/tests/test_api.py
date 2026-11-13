from fastapi.testclient import TestClient

import app.api.routes as routes
from app.crew import pick_engine
from app.main import app
from app.utils import extract_code

client = TestClient(app)


def test_health():
    assert client.get("/api/health").json() == {"status": "ok"}


def test_run_returns_final_code(monkeypatch):
    fake = {"stages": [], "final_code": "print('hi')", "report": "# Report"}
    monkeypatch.setattr(routes, "run_pipeline", lambda *a, **k: fake)
    r = client.post("/api/run", json={"requirement": "Build a simple calculator CLI"})
    assert r.status_code == 200
    assert r.json()["final_code"] == "print('hi')"


def test_short_requirement_rejected():
    assert client.post("/api/run", json={"requirement": "hi"}).status_code == 422


def test_pipeline_failure_returns_502(monkeypatch):
    def boom(*a, **k):
        raise RuntimeError("llm down")
    monkeypatch.setattr(routes, "run_pipeline", boom)
    assert client.post("/api/run", json={"requirement": "Build a todo app please"}).status_code == 502


def test_extract_code_picks_longest_block():
    text = "```python\nx=1\n```\ntext\n```python\nprint('a')\nprint('b')\n```"
    assert "print('b')" in extract_code(text)


def test_engine_auto_falls_back_to_groq(monkeypatch):
    import importlib.util

    monkeypatch.setattr(importlib.util, "find_spec", lambda name: None)
    assert pick_engine("auto") == "groq"
    assert pick_engine("crewai") == "crewai"


def test_unknown_engine_rejected():
    import pytest

    with pytest.raises(ValueError):
        pick_engine("nope")


def test_extract_code_handles_cut_off_block():
    assert extract_code("```python\nprint(1)\nprint(2)") == "print(1)\nprint(2)"
