"""DEVELOPMENT ONLY: preview the Ask page's states with mocked /ask responses.

Serves the real frontend files beside a fake /ask; needs no database or LM Studio.
The production app never imports this file. From the project root, run:

    python -m scripts.preview_frontend

Then open http://127.0.0.1:8001/?state=<state> and press Ask, where <state> is
success, insufficient, error, timeout, or loading.
"""

import asyncio
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from schemas.answer import AskResponse, Evidence, Fact

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
INSUFFICIENT_ANSWER = "The available evidence is insufficient to answer this question."
ERRORS = {"error": 503, "timeout": 504}

app = FastAPI(title="MythosAI frontend preview (mock data)")
app.mount("/assets", StaticFiles(directory=FRONTEND_DIR), name="assets")


@app.get("/", include_in_schema=False)
def ask_page():
    return FileResponse(FRONTEND_DIR / "index.html")


def mock_answer(question: str, insufficient: bool) -> AskResponse:
    """Built through the real response schema so the mock cannot drift from the contract."""
    if insufficient:
        return AskResponse(
            question=question,
            answer=INSUFFICIENT_ANSWER,
            insufficient_context=True,
            facts=[],
            evidence=[],
        )
    fact = {"entity_type": "character", "entity_id": 1, "name": "Percy Jackson"}
    return AskResponse(
        question=question,
        answer="MOCK PREVIEW: Percy Jackson is a son of Poseidon with water-related powers.",
        insufficient_context=False,
        facts=[
            Fact(**fact, field="parent_god", value="Poseidon"),
            Fact(**fact, field="power:1", value="Hydrokinesis: Control over water."),
        ],
        evidence=[
            Evidence(
                source_id="mock-percy",
                title="Percy Jackson (mock passage)",
                reference="Mock preview data, not from the corpus",
                text="Percy Jackson is a demigod son of Poseidon.",
                tags=["mock"],
                score=0.5,
            )
        ],
    )


@app.post("/ask")
async def ask(request: Request):
    # The state comes from the page URL (?state=...), which the browser sends as the Referer.
    page_query = parse_qs(urlparse(request.headers.get("referer", "")).query)
    state = page_query.get("state", ["success"])[0]
    question = str((await request.json()).get("question", "")).strip()
    await asyncio.sleep(300 if state == "loading" else 1)
    if state in ERRORS:
        return JSONResponse({"detail": "Mock preview error."}, status_code=ERRORS[state])
    return mock_answer(question, insufficient=state == "insufficient")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
