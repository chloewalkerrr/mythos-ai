"""Request and response contracts for the grounded-answer endpoint."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from retrieval import Source


class AskRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    question: str = Field(strict=True, min_length=1, max_length=2000)

    @field_validator("question")
    @classmethod
    def require_words(cls, value: str) -> str:
        if not any(character.isalpha() for character in value):
            raise ValueError("Question must contain words")
        return value


class Fact(BaseModel):
    entity_type: Literal["character", "god"]
    entity_id: int
    name: str
    field: str
    value: str


class Evidence(Source):
    score: float
    provenance: Literal["development_summary"] = "development_summary"


class GeneratedAnswer(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    answer: str
    insufficient_context: bool


class AskResponse(GeneratedAnswer):
    question: str
    facts: list[Fact]
    evidence: list[Evidence]
