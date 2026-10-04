from pydantic import BaseModel, Field


class LocationCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    location_type: str | None = None
    description: str | None = None
    coordinates: str | None = None
    realm: str | None = None


class LocationUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    location_type: str | None = None
    description: str | None = None
    coordinates: str | None = None
    realm: str | None = None


class LocationResponse(BaseModel):
    id: int
    name: str
    location_type: str | None = None
    description: str | None = None
    coordinates: str | None = None
    realm: str | None = None

    model_config = {
        "from_attributes": True,
    }
