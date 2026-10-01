import json

import pytest

from retrieval import load_corpus, retrieve


def write_corpus(tmp_path, records):
    path = tmp_path / "sources.json"
    path.write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")
    return path


def test_load_starter_corpus_from_another_working_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    sources = load_corpus()

    assert sources
    assert len({source.source_id for source in sources}) == len(sources)
    medusa = next(source for source in sources if source.source_id == "medusa-gaze")
    assert medusa.title == "Medusa and her petrifying gaze"
    assert "scripts/populate_data.py" in medusa.reference
    assert "turns people to stone" in medusa.text
    assert "Medusa" in medusa.tags


def test_load_minimal_utf8_source_without_tags(tmp_path):
    record = {
        "source_id": "athena",
        "title": "Athéna",
        "reference": "Project note",
        "text": "Wisdom",
    }
    sources = load_corpus(write_corpus(tmp_path, [record]))

    assert sources[0].title == "Athéna"
    assert sources[0].tags == []


@pytest.mark.parametrize(
    "records",
    [
        {},
        [{"title": "Missing fields"}],
        [{"source_id": "id", "title": "Title", "reference": "Note", "text": "  "}],
        [{"source_id": "id", "title": "Title", "reference": "", "text": "Text"}],
        [{"source_id": 1, "title": "Title", "reference": "Note", "text": "Text"}],
        [{"source_id": "id", "title": "Title", "reference": "Note", "text": "Text", "tags": "god"}],
    ],
)
def test_load_rejects_invalid_records(tmp_path, records):
    with pytest.raises(ValueError):
        load_corpus(write_corpus(tmp_path, records))


def test_load_rejects_duplicate_source_ids(tmp_path):
    record = {"source_id": "same", "title": "Title", "reference": "Note", "text": "Text"}
    with pytest.raises(ValueError, match="unique"):
        load_corpus(write_corpus(tmp_path, [record, record]))


def test_load_rejects_malformed_json(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("not json", encoding="utf-8")
    with pytest.raises(ValueError):
        load_corpus(path)


@pytest.mark.parametrize(
    ("query", "expected_id"),
    [
        ("Which monster turns people to stone?", "medusa-gaze"),
        ("Who is the god of the sea?", "poseidon-domains"),
        ("What water powers does Percy Jackson have?", "percy-water-powers"),
    ],
)
def test_retrieve_relevant_passage(query, expected_id):
    results = retrieve(query, top_k=2)

    assert 1 <= len(results) <= 2
    assert results[0].source.source_id == expected_id
    assert results[0].source.reference
    assert results[0].source.text
    assert all(result.score > 0 for result in results)
    assert [result.score for result in results] == sorted(
        (result.score for result in results), reverse=True
    )


def test_wisdom_query_ranks_athena_without_poseidon_contamination():
    results = retrieve("goddess of wisdom", top_k=len(load_corpus()))

    assert results[0].source.source_id == "athena-wisdom"
    assert results[0].score > 0
    assert "poseidon-domains" not in [result.source.source_id for result in results]


def test_ordering_is_repeatable():
    assert retrieve("Poseidon Percy sea horses") == retrieve("Poseidon Percy sea horses")


def test_equal_scores_use_source_id_regardless_of_file_order(tmp_path):
    records = [
        {"source_id": source_id, "title": "Sea", "reference": "Note", "text": "Water"}
        for source_id in ["b", "a"]
    ]
    path = write_corpus(tmp_path, records)
    results = retrieve("sea", corpus_path=path)
    assert [result.source.source_id for result in results] == ["a", "b"]
    assert results[0].score == results[1].score
    write_corpus(tmp_path, list(reversed(records)))
    assert retrieve("sea", corpus_path=path) == results
    assert retrieve("sea", top_k=1, corpus_path=path) == results[:1]


def test_case_and_punctuation_are_normalized():
    assert retrieve("MEDUSA!!!") == retrieve("medusa")


@pytest.mark.parametrize("query", ["", " \n\t ", "?!", "who is the", "spaceshipxyz"])
def test_empty_or_unmatched_queries_return_no_results(query):
    assert retrieve(query) == []


@pytest.mark.parametrize("query", [None, 42, ["Medusa"]])
def test_non_string_queries_are_rejected(query):
    with pytest.raises(TypeError, match="query must be a string"):
        retrieve(query)


@pytest.mark.parametrize("top_k", [0, -1, 1.5, True])
def test_invalid_result_limits_are_rejected(top_k):
    with pytest.raises(ValueError, match="positive integer"):
        retrieve("Medusa", top_k=top_k)


def test_empty_corpus_returns_no_results(tmp_path):
    path = write_corpus(tmp_path, [])
    assert load_corpus(path) == []
    assert retrieve("Medusa", corpus_path=path) == []
