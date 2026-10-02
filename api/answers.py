"""Grounded answers from the local corpus and selected relational facts."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import llm
from answer_context import database_facts
from models import get_db
from retrieval import retrieve
from schemas.answer import AskRequest, AskResponse, Evidence, GeneratedAnswer

router = APIRouter(tags=["Answers"])


@router.post("/ask", response_model=AskResponse)
def ask(request: AskRequest, db: Session = Depends(get_db)):
    evidence = [
        Evidence(**result.source.model_dump(), score=result.score)
        for result in retrieve(request.question, top_k=3)
    ]
    facts = database_facts(request.question, db)
    result = GeneratedAnswer(answer=llm.INSUFFICIENT_ANSWER, insufficient_context=True)
    if facts or evidence:
        try:
            result = llm.generate_answer(request.question, facts, evidence)
        except llm.ProviderError as exc:
            raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc
    return AskResponse(
        question=request.question,
        answer=llm.INSUFFICIENT_ANSWER if result.insufficient_context else result.answer,
        insufficient_context=result.insufficient_context,
        facts=facts,
        evidence=evidence,
    )
