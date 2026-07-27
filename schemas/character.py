from pydantic import BaseModel, Field


class CharacterCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=150)


class CharacterUpdate(BaseModel):
    status: str = Field(min_length=1, max_length=100)
