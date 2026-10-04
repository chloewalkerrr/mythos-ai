from pydantic import BaseModel, Field

from models.all_models import MonsterThreatLevel


class MonsterCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    species: str | None = None
    threat_level: MonsterThreatLevel | None = None
    description: str | None = None
    weaknesses: str | None = None
    abilities: str | None = None


class MonsterUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    species: str | None = None
    threat_level: MonsterThreatLevel | None = None
    description: str | None = None
    weaknesses: str | None = None
    abilities: str | None = None


class MonsterResponse(BaseModel):
    id: int
    name: str
    species: str | None = None
    threat_level: MonsterThreatLevel | None = None
    description: str | None = None
    weaknesses: str | None = None
    abilities: str | None = None

    model_config = {
        "from_attributes": True,
    }
