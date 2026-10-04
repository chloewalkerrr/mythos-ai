from pydantic import BaseModel


class CabinCreate(BaseModel):
    cabin_number: int
    patron_god_id: int
    description: str | None = None
    color_scheme: str | None = None


class CabinUpdate(BaseModel):
    cabin_number: int | None = None
    patron_god_id: int | None = None
    description: str | None = None
    color_scheme: str | None = None


class CabinResponse(BaseModel):
    id: int
    cabin_number: int | None = None
    patron_god_id: int | None = None
    description: str | None = None
    color_scheme: str | None = None

    model_config = {
        "from_attributes": True,
    }
