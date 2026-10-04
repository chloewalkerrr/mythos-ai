from pydantic import BaseModel, Field


class GodCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    roman_name: str | None = None
    title: str | None = None
    domain: str | None = None
    symbol: str | None = None
    description: str | None = None


class GodUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    roman_name: str | None = None
    title: str | None = None
    domain: str | None = None
    symbol: str | None = None
    description: str | None = None


class GodResponse(BaseModel):
    id: int
    name: str
    roman_name: str | None = None
    title: str | None = None
    domain: str | None = None
    symbol: str | None = None
    description: str | None = None

    model_config = {
        "from_attributes": True,
    }
