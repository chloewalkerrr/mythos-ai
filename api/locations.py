from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import get_db
from models.all_models import Location
from schemas.location import LocationCreate, LocationResponse, LocationUpdate

router = APIRouter(
    prefix="/locations",
    tags=["Locations"],
)


@router.get("", response_model=list[LocationResponse])
def get_locations(db: Session = Depends(get_db)):
    return db.query(Location).all()


@router.get("/{id}", response_model=LocationResponse)
def get_location(id: int, db: Session = Depends(get_db)):
    location = db.query(Location).filter(Location.id == id).first()

    if not location:
        raise HTTPException(status_code=404, detail="Not found")

    return location


@router.post("", response_model=LocationResponse)
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    new_location = Location(**location.model_dump())

    db.add(new_location)
    db.commit()
    db.refresh(new_location)

    return new_location


@router.put("/{id}", response_model=LocationResponse)
def update_location(id: int, location: LocationUpdate, db: Session = Depends(get_db)):
    existing = db.query(Location).filter(Location.id == id).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Not found")

    for field, value in location.model_dump(exclude_unset=True).items():
        setattr(existing, field, value)

    db.commit()
    db.refresh(existing)

    return existing


@router.delete("/{id}")
def delete_location(id: int, db: Session = Depends(get_db)):
    location = db.query(Location).filter(Location.id == id).first()

    if not location:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(location)
    db.commit()

    return {"message": "Deleted"}
