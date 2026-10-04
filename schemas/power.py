from pydantic import BaseModel, Field


class PowerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None
    power_type: str | None = None
    power_level: int | None = Field(default=None, ge=1, le=10)


class PowerUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    power_type: str | None = None
    power_level: int | None = Field(default=None, ge=1, le=10)


class PowerResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    power_type: str | None = None
    power_level: int | None = None

    model_config = {
        "from_attributes": True,
    }
