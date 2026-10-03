"""Test the offline measurement, without requiring every benchmark case to pass."""

import hashlib
from collections import Counter

import pytest

import llm
from scripts import evaluate


def test_fixed_case_set():
    cases = evaluate.load_cases()
    assert len(cases) == 18
    assert Counter(case.category for case in cases) == {
        "direct": 6,
        "paraphrase": 4,
        "complementary": 4,
        "unsupported_no_context": 2,
        "unsupported_related": 2,
    }


def test_evaluation_is_repeatable_and_never_calls_model(monkeypatch):
    def unexpected_model_call(*args, **kwargs):
        pytest.fail("Offline evaluation must not generate answers")

    monkeypatch.setattr(llm, "generate_answer", unexpected_model_call)
    first = evaluate.run_evaluation()
    assert first == evaluate.run_evaluation()
    assert first["cases_checked"] == 18
    assert first["summary"]["expected_evidence_in_top3"]["checked"] == 14
    assert all(row["model_answerability"] == "not_evaluated" for row in first["cases"])


def test_file_hash_ignores_line_endings(tmp_path):
    lf, crlf = tmp_path / "lf.json", tmp_path / "crlf.json"
    lf.write_bytes(b'[\n  {"id": "01"}\n]\n')
    crlf.write_bytes(b'[\r\n  {"id": "01"}\r\n]\r\n')
    assert evaluate.file_sha256(crlf) == evaluate.file_sha256(lf)
    assert evaluate.file_sha256(lf) == hashlib.sha256(lf.read_bytes()).hexdigest()


def test_missed_evidence_is_reported_as_failure(monkeypatch):
    case = evaluate.load_cases()[0]
    monkeypatch.setattr(evaluate, "retrieve", lambda *args, **kwargs: [])
    with evaluate.fixture_session() as db:
        result = evaluate.evaluate_case(case, db)
    assert result["passed"] is False
    assert result["checks"]["expected_evidence_in_top3"] is False
    assert result["missing_source_ids"] == ["percy-parentage"]
    assert result["checks"]["expected_facts"] is True


@pytest.mark.parametrize(
    "case",
    [case for case in evaluate.load_cases() if case.category == "unsupported_no_context"],
    ids=lambda case: case.id,
)
def test_unmatched_cases_short_circuit_real_ask_route(client, monkeypatch, case):
    def unexpected_model_call(*args, **kwargs):
        pytest.fail("No context should skip the provider")

    monkeypatch.setattr(llm, "generate_answer", unexpected_model_call)
    response = client.post("/ask", json={"question": case.question})
    assert response.status_code == 200
    assert response.json()["insufficient_context"] is True
    assert response.json()["facts"] == response.json()["evidence"] == []


@pytest.mark.parametrize(
    "case",
    [case for case in evaluate.load_cases() if case.category == "unsupported_related"],
    ids=lambda case: case.id,
)
def test_related_context_does_not_count_as_verified_answerability(case):
    with evaluate.fixture_session() as db:
        result = evaluate.evaluate_case(case, db)
    assert result["selected_facts"] and result["retrieved_source_ids"]
    assert result["automatic_insufficient_context"] is False
    assert result["checks"]["expected_evidence_in_top3"] is None
    assert result["model_answerability"] == "not_evaluated"
