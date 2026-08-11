from pydantic import BaseModel, Field


class WeaponCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    weapon_type: str | None = None
    material: str | None = None
    description: str | None = None
    special_abilities: str | None = None
    owner_id: int | None = None


class WeaponUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    weapon_type: str | None = None
    material: str | None = None
    description: str | None = None
    special_abilities: str | None = None
    owner_id: int | None = None


class WeaponResponse(BaseModel):
    id: int
    name: str
    weapon_type: str | None = None
    material: str | None = None
    description: str | None = None
    special_abilities: str | None = None
    owner_id: int | None = None

    model_config = {
        "from_attributes": True,
    }
