"""Exercise the complete answer flow with an HTTP-level provider fake."""

import json

import httpx
import pytest

import llm
from answer_context import database_facts
from models.character import Character
from models.config import Settings
from retrieval import retrieve
from schemas.answer import GeneratedAnswer


def provider_response(answer="Percy Jackson's parent is Poseidon.", insufficient=False):
    return {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": json.dumps({"answer": answer, "insufficient_context": insufficient}),
                },
            }
        ],
    }


@pytest.fixture(autouse=True)
def fake_provider(monkeypatch):
    calls = []
    monkeypatch.delenv("LM_STUDIO_BASE_URL", raising=False)
    monkeypatch.delenv("LM_STUDIO_MODEL", raising=False)
    monkeypatch.delenv("LM_STUDIO_TIMEOUT_SECONDS", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(llm, "settings", Settings(_env_file=None, db_user="test", db_name="test"))

    def post(url, **kwargs):
        calls.append({"url": url, **kwargs})
        return httpx.Response(200, json=provider_response(), request=httpx.Request("POST", url))

    monkeypatch.setattr(llm.httpx, "post", post)
    return calls


def test_ask_returns_exact_context_sent_to_provider(client, sample_data, fake_provider):
    question = "Who is Percy Jackson's parent?"
    response = client.post("/ask", json={"question": f"  {question}  "})
    assert response.status_code == 200
    body = response.json()
    assert set(body) == {"question", "answer", "insufficient_context", "facts", "evidence"}
    assert body["question"] == question
    assert body["answer"] == "Percy Jackson's parent is Poseidon."
    assert body["insufficient_context"] is False
    assert any(f["field"] == "parent_god" and f["value"] == "Poseidon" for f in body["facts"])
    assert any("Hydrokinesis" in f["value"] for f in body["facts"])
    assert all(f["name"] == "Percy Jackson" for f in body["facts"])
    expected = retrieve(question)
    assert [p["source_id"] for p in body["evidence"]] == [p.source.source_id for p in expected]
    for passage, result in zip(body["evidence"], expected, strict=True):
        assert passage == {
            **result.source.model_dump(),
            "score": result.score,
            "provenance": "attributed_summary",
        }
    assert all(p["provenance"] == "attributed_summary" for p in body["evidence"])
    assert all(p["source_url"].startswith("https://rickriordan.com/") for p in body["evidence"])
    assert all("source_url" not in fact for fact in body["facts"])
    assert len(fake_provider) == 1
    call = fake_provider[0]
    assert call["url"] == "http://127.0.0.1:1234/v1/chat/completions"
    assert "headers" not in call
    assert call["timeout"] == 120.0
    payload = call["json"]
    assert payload["model"] == "qwen/qwen3-4b-2507"
    assert payload["max_tokens"] == 800
    assert payload["stream"] is False
    context = json.loads(payload["messages"][1]["content"])
    assert context == {key: body[key] for key in ("question", "facts", "evidence")}
    assert "not direct quotations" in payload["messages"][0]["content"]
    assert "not to database facts" in payload["messages"][0]["content"]
    assert payload["response_format"] == {
        "type": "json_schema",
        "json_schema": {"name": "grounded_answer", "schema": GeneratedAnswer.model_json_schema()},
    }


def test_retrieval_without_database_matches(client, fake_provider):
    response = client.post("/ask", json={"question": "Who is the goddess of wisdom?"})
    assert response.status_code == 200
    assert response.json()["facts"] == []
    assert response.json()["evidence"][0]["source_id"] == "athena-wisdom"
    assert len(fake_provider) == 1


def test_database_matches_are_deterministic_and_unambiguous(db_session, sample_data):
    facts = database_facts("Tell me about Neptune and Percy", db_session)
    assert any(f.field == "domain" and f.value == "Sea" for f in facts)
    assert {f.name for f in facts} == {"Poseidon", "Percy Jackson"}
    assert facts == database_facts("Tell me about Neptune and Percy", db_session)
    assert database_facts("Percyish Neptuneworld", db_session) == []
    db_session.add_all([Character(name="Percy Smith"), Character(name="")])
    db_session.commit()
    assert database_facts("Who is Percy?", db_session) == []
    assert database_facts("Who is Percy Jackson?", db_session)


@pytest.mark.parametrize("question", ["", "   ", "?!", 123, None, "x" * 2001])
def test_invalid_question(client, fake_provider, question):
    assert client.post("/ask", json={"question": question}).status_code == 422
    assert fake_provider == []


def test_missing_question(client, fake_provider):
    assert client.post("/ask", json={}).status_code == 422
    assert fake_provider == []


def test_no_context_skips_provider(client, fake_provider):
    response = client.post("/ask", json={"question": "Explain quarks"})
    assert response.status_code == 200
    assert response.json() == {
        "question": "Explain quarks",
        "answer": llm.INSUFFICIENT_ANSWER,
        "insufficient_context": True,
        "facts": [],
        "evidence": [],
    }
    assert fake_provider == []


def test_provider_can_report_insufficient_context(client, sample_data, monkeypatch):
    def post(url, **kwargs):
        return httpx.Response(
            200,
            json=provider_response("Insufficient evidence.", insufficient=True),
            request=httpx.Request("POST", url),
        )

    monkeypatch.setattr(llm.httpx, "post", post)
    response = client.post("/ask", json={"question": "What is Percy's favorite breakfast?"})
    assert response.status_code == 200
    assert response.json()["insufficient_context"] is True
    assert response.json()["answer"] == llm.INSUFFICIENT_ANSWER
    assert response.json()["facts"]
    assert response.json()["evidence"]


def test_local_configuration_from_environment(client, monkeypatch, fake_provider):
    monkeypatch.setenv("LM_STUDIO_BASE_URL", "http://127.0.0.1:4321/")
    monkeypatch.setenv("LM_STUDIO_MODEL", "local-test-model")
    monkeypatch.setenv("LM_STUDIO_TIMEOUT_SECONDS", "180")
    monkeypatch.setattr(llm, "settings", Settings(_env_file=None, db_user="test", db_name="test"))
    assert client.post("/ask", json={"question": "Who is Athena?"}).status_code == 200
    assert fake_provider[0]["url"] == "http://127.0.0.1:4321/v1/chat/completions"
    assert fake_provider[0]["json"]["model"] == "local-test-model"
    assert fake_provider[0]["timeout"] == 180.0


@pytest.mark.parametrize(
    ("error", "status", "detail"),
    [
        (
            httpx.ConnectError("private upstream detail"),
            503,
            "Local model server is unavailable. Start LM Studio's server.",
        ),
        (httpx.ReadTimeout("private timeout"), 504, "Local model server timed out."),
        (httpx.ConnectTimeout("private timeout"), 504, "Local model server timed out."),
    ],
)
def test_network_failure(client, monkeypatch, error, status, detail):
    def post(*args, **kwargs):
        raise error

    monkeypatch.setattr(llm.httpx, "post", post)
    response = client.post("/ask", json={"question": "Who is Athena?"})
    assert response.status_code == status
    assert response.json() == {"detail": detail}
    assert "private" not in response.text


@pytest.mark.parametrize(
    ("status", "body"),
    [
        (429, {"error": "private upstream detail"}),
        (200, {"choices": [{"finish_reason": "length", "message": {"content": "{}"}}]}),
        (200, {"choices": []}),
        (
            200,
            {
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {"content": None, "refusal": "Cannot answer"},
                    }
                ],
            },
        ),
        (200, provider_response(answer="")),
        (200, provider_response(answer=" \n\t ")),
        (200, provider_response(insufficient="false")),
        (200, []),
    ],
)
def test_bad_provider_response(client, monkeypatch, status, body):
    def post(url, **kwargs):
        return httpx.Response(status, json=body, request=httpx.Request("POST", url))

    monkeypatch.setattr(llm.httpx, "post", post)
    response = client.post("/ask", json={"question": "Who is Athena?"})
    assert response.status_code == 502
    assert set(response.json()) == {"detail"}
    assert "private" not in response.text


@pytest.mark.parametrize(
    "content",
    [
        "not JSON",
        '{"answer": "unfinished',
        '{"answer": "Missing flag"}',
        '{"answer": "Invented context", "insufficient_context": false, "facts": []}',
        '{"answer": "Invented citations", "insufficient_context": false, "evidence": []}',
        None,
        [],
    ],
)
def test_invalid_generated_content(client, monkeypatch, content):
    body = provider_response()
    body["choices"][0]["message"]["content"] = content

    def post(url, **kwargs):
        return httpx.Response(200, json=body, request=httpx.Request("POST", url))

    monkeypatch.setattr(llm.httpx, "post", post)
    response = client.post("/ask", json={"question": "Who is Athena?"})
    assert response.status_code == 502
    assert response.json() == {"detail": "Local model server returned an invalid response."}


def test_non_json_server_response(client, monkeypatch):
    def post(url, **kwargs):
        return httpx.Response(200, text="private invalid body", request=httpx.Request("POST", url))

    monkeypatch.setattr(llm.httpx, "post", post)
    response = client.post("/ask", json={"question": "Who is Athena?"})
    assert response.status_code == 502
    assert response.json() == {"detail": "Local model server returned an invalid response."}
