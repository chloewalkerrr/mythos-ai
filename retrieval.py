"""Local passage retrieval using TF-IDF cosine similarity; no database required."""

import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, TypeAdapter, field_validator

DEFAULT_CORPUS_PATH = Path(__file__).resolve().parent / "corpus" / "sources.json"
STOP_WORDS = frozenset(
    "a an and are as at be by can do does for from how in is it of on or that the "
    "their this to was were what which who with".split()
)


class Source(BaseModel):
    """One curated passage and the metadata needed to identify its evidence."""

    model_config = ConfigDict(strict=True, extra="forbid", str_strip_whitespace=True)

    source_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    reference: str = Field(min_length=1)
    source_url: str
    provenance: Literal["attributed_summary"]
    text: str = Field(min_length=1)
    tags: list[str] = Field(default_factory=list)

    @field_validator("source_url")
    @classmethod
    def require_source_url(cls, value: str) -> str:
        url = HttpUrl(value)
        if url.username or url.password:
            raise ValueError("Source URLs must not contain credentials")
        # Keep URLs JSON-native throughout the existing context and HTTP boundary.
        return str(url)


@dataclass(frozen=True)
class RetrievalResult:
    source: Source
    score: float


def load_corpus(path: str | Path = DEFAULT_CORPUS_PATH) -> list[Source]:
    """Read a UTF-8 JSON array; reject malformed records and duplicate source IDs."""
    sources = TypeAdapter(list[Source]).validate_json(Path(path).read_text(encoding="utf-8"))
    source_ids = [source.source_id for source in sources]
    if len(source_ids) != len(set(source_ids)):
        raise ValueError("Corpus source_id values must be unique")
    return sources


def _tokens(text: str) -> list[str]:
    return [word for word in re.findall(r"[^\W_]{2,}", text.casefold()) if word not in STOP_WORDS]


def _tfidf(counts: Counter[str], idf: dict[str, float]) -> dict[str, float]:
    weights = {term: counts[term] * idf[term] for term in sorted(counts) if term in idf}
    length = math.sqrt(sum(weight * weight for weight in weights.values()))
    return {term: weight / length for term, weight in weights.items()} if length else {}


def retrieve(
    query: str,
    *,
    top_k: int = 3,
    corpus_path: str | Path = DEFAULT_CORPUS_PATH,
) -> list[RetrievalResult]:
    """Return positive-scoring matches, ordered by descending score then source ID.

    Blank, stop-word-only, and unmatched queries return an empty list.
    Non-string queries raise TypeError; top_k must be a positive integer.
    Scores indicate lexical similarity, not factual confidence.
    """
    if not isinstance(query, str):
        raise TypeError("query must be a string")
    if isinstance(top_k, bool) or not isinstance(top_k, int) or top_k < 1:
        raise ValueError("top_k must be a positive integer")
    query_counts = Counter(_tokens(query))
    if not query_counts:
        return []

    sources = load_corpus(corpus_path)
    documents = [Counter(_tokens(" ".join([s.title, s.text, *s.tags]))) for s in sources]
    document_frequency = Counter(term for document in documents for term in document)
    idf = {
        term: math.log((1 + len(documents)) / (1 + frequency)) + 1
        for term, frequency in document_frequency.items()
    }
    query_vector = _tfidf(query_counts, idf)
    if not query_vector:
        return []

    results = []
    for source, document in zip(sources, documents, strict=True):
        vector = _tfidf(document, idf)
        score = sum(weight * vector.get(term, 0.0) for term, weight in query_vector.items())
        if score > 0:
            results.append(RetrievalResult(source=source, score=score))
    return sorted(results, key=lambda result: (-result.score, result.source.source_id))[:top_k]
