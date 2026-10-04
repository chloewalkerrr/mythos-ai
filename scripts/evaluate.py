"""Run offline context checks: python -m scripts.evaluate --output evaluation/results.json.

Exit 1 means benchmark checks failed, not that a model answer was scored.
No application database connections, HTTP calls, or generated answers are used.
"""

import argparse
import hashlib
import json
from contextlib import contextmanager
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from answer_context import database_facts
from models import Base, Character, CharacterPower, God, Power
from retrieval import DEFAULT_CORPUS_PATH, load_corpus, retrieve

CASES_PATH = Path(__file__).resolve().parent.parent / "evaluation" / "cases.json"


class ExpectedFact(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")
    name: str
    field: str
    value: str


class EvaluationCase(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")
    id: str
    category: Literal[
        "direct", "paraphrase", "complementary", "unsupported_no_context", "unsupported_related"
    ]
    question: str = Field(min_length=1, max_length=2000)
    expected_source_ids: list[str]
    expected_entities: list[str]
    expected_facts: list[ExpectedFact]
    expected_auto_insufficient: bool


def load_cases(path: Path = CASES_PATH) -> list[EvaluationCase]:
    cases = TypeAdapter(list[EvaluationCase]).validate_json(path.read_text(encoding="utf-8"))
    if len({case.id for case in cases}) != len(cases):
        raise ValueError("Evaluation case IDs must be unique")
    source_ids = {source.source_id for source in load_corpus()}
    for case in cases:
        if not set(case.expected_source_ids) <= source_ids:
            raise ValueError(f"Unknown expected source ID in case {case.id}")
    return cases


def file_sha256(path: Path) -> str:
    """Hash with LF line endings so Git checkouts on any platform match."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


@contextmanager
def fixture_session():
    """A fixed subset of scripts/populate_data.py, not externally attributed evidence.

    Only two gods, two characters, and two powers are needed for these cases.
    Explicit IDs keep power fields stable. Never use the application's SessionLocal.
    """
    engine = create_engine("sqlite://")
    try:
        Base.metadata.create_all(engine)
        with Session(engine) as db:
            db.add_all(
                [
                    God(
                        id=2,
                        name="Poseidon",
                        roman_name="Neptune",
                        title="God of the Sea",
                        domain="Sea, Earthquakes, Horses",
                        symbol="Trident",
                        description="God of the sea, earthquakes, and horses",
                    ),
                    God(
                        id=4,
                        name="Athena",
                        roman_name="Minerva",
                        title="Goddess of Wisdom",
                        domain="Wisdom, Battle Strategy, Crafts",
                        symbol="Owl",
                        description="Goddess of wisdom and strategic warfare",
                    ),
                    Character(
                        id=1,
                        name="Percy Jackson",
                        parent_god_id=2,
                        description="Son of Poseidon, main protagonist",
                    ),
                    Character(
                        id=2,
                        name="Annabeth Chase",
                        parent_god_id=4,
                        description="Daughter of Athena, architect and strategist",
                    ),
                    Power(
                        id=1,
                        name="Hydrokinesis",
                        description="Control over water and related phenomena",
                    ),
                    Power(
                        id=2,
                        name="Strategic Mind",
                        description="Enhanced tactical and strategic thinking",
                    ),
                    CharacterPower(character_id=1, power_id=1),
                    CharacterPower(character_id=2, power_id=2),
                ]
            )
            db.commit()
            yield db
    finally:
        engine.dispose()


def evaluate_case(case: EvaluationCase, db: Session) -> dict:
    results = retrieve(case.question, top_k=3)
    facts = database_facts(case.question, db)
    retrieved_ids = [result.source.source_id for result in results]
    entities = sorted({fact.name for fact in facts})
    fact_keys = {(fact.name, fact.field, fact.value) for fact in facts}
    missing_sources = sorted(set(case.expected_source_ids) - set(retrieved_ids))
    missing_facts = [
        fact.model_dump()
        for fact in case.expected_facts
        if (fact.name, fact.field, fact.value) not in fact_keys
    ]
    # This is only the API's deterministic empty-context gate, not answerability.
    auto_insufficient = not facts and not results
    checks = {
        "expected_evidence_in_top3": not missing_sources if case.expected_source_ids else None,
        "exact_entities": entities == sorted(case.expected_entities),
        "expected_facts": not missing_facts if case.expected_facts else None,
        "empty_context_gate": auto_insufficient == case.expected_auto_insufficient,
    }
    return {
        **case.model_dump(),
        "retrieved_source_ids": retrieved_ids,
        "selected_entities": entities,
        "selected_facts": [fact.model_dump() for fact in facts],
        "missing_source_ids": missing_sources,
        "missing_facts": missing_facts,
        "automatic_insufficient_context": auto_insufficient,
        "model_answerability": "not_evaluated",
        "checks": checks,
        "passed": all(value is not False for value in checks.values()),
    }


def run_evaluation() -> dict:
    cases = load_cases()
    with fixture_session() as db:
        rows = [evaluate_case(case, db) for case in cases]
    summary = {}
    for check in rows[0]["checks"]:
        values = [row["checks"][check] for row in rows if row["checks"][check] is not None]
        summary[check] = {"passed": sum(values), "checked": len(values)}
    return {
        "scope": "Deterministic retrieval and DB-context checks; no generated answers evaluated.",
        "fixture": "In-memory SQLite subset of demo data: 2 gods, 2 characters, 2 powers.",
        "limitations": [
            "These 18 hand-authored cases are a small regression set, "
            "not a general accuracy estimate.",
            "Related context can exist for an unsupported question; "
            "model refusal is not tested here.",
            "Empty-context checks verify the gate condition; "
            "API behavior is covered by mocked tests.",
            "Database facts are project data and are not certified by the attributed evidence.",
        ],
        "corpus_sha256": file_sha256(DEFAULT_CORPUS_PATH),
        "cases_sha256": file_sha256(CASES_PATH),
        "summary": summary,
        "cases_passed": sum(row["passed"] for row in rows),
        "cases_checked": len(rows),
        "cases": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Also save the complete JSON report")
    args = parser.parse_args()
    report = run_evaluation()
    output = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(output + "\n", encoding="utf-8")
    print(output)
    return 0 if report["cases_passed"] == report["cases_checked"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
