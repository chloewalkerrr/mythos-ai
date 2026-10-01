from pydantic import BaseModel, Field

from models.character import CharacterStatus


class CharacterCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=150)


class CharacterUpdate(BaseModel):
    status: CharacterStatus


class CharacterResponse(BaseModel):
    id: int
    name: str
    age: int | None = None
    gender: str | None = None
    status: str | None = None

    model_config = {
        "from_attributes": True,
    }
