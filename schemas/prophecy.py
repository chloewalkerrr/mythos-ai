from datetime import date

from pydantic import BaseModel, Field


class ProphecyCreate(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    text: str = Field(min_length=1)
    speaker: str | None = None
    date_spoken: date | None = None
    interpretation: str | None = None
    fulfilled: bool = False


class ProphecyUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    text: str | None = Field(default=None, min_length=1)
    speaker: str | None = None
    date_spoken: date | None = None
    interpretation: str | None = None
    fulfilled: bool | None = None


class ProphecyResponse(BaseModel):
    id: int
    title: str | None = None
    text: str
    speaker: str | None = None
    date_spoken: date | None = None
    interpretation: str | None = None
    fulfilled: bool

    model_config = {
        "from_attributes": True,
    }
