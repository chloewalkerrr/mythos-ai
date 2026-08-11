from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import get_db
from models.all_models import Cabin
from schemas.cabin import CabinCreate, CabinResponse, CabinUpdate

router = APIRouter(
    prefix="/cabins",
    tags=["Cabins"],
)


@router.get("", response_model=list[CabinResponse])
def get_cabins(db: Session = Depends(get_db)):
    return db.query(Cabin).all()


@router.get("/{id}", response_model=CabinResponse)
def get_cabin(id: int, db: Session = Depends(get_db)):
    cabin = db.query(Cabin).filter(Cabin.id == id).first()

    if not cabin:
        raise HTTPException(status_code=404, detail="Not found")

    return cabin


@router.post("", response_model=CabinResponse)
def create_cabin(cabin: CabinCreate, db: Session = Depends(get_db)):
    new_cabin = Cabin(**cabin.model_dump())

    db.add(new_cabin)
    db.commit()
    db.refresh(new_cabin)

    return new_cabin


@router.put("/{id}", response_model=CabinResponse)
def update_cabin(id: int, cabin: CabinUpdate, db: Session = Depends(get_db)):
    existing = db.query(Cabin).filter(Cabin.id == id).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Not found")

    for field, value in cabin.model_dump(exclude_unset=True).items():
        setattr(existing, field, value)

    db.commit()
    db.refresh(existing)

    return existing


@router.delete("/{id}")
def delete_cabin(id: int, db: Session = Depends(get_db)):
    cabin = db.query(Cabin).filter(Cabin.id == id).first()

    if not cabin:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(cabin)
    db.commit()

    return {"message": "Deleted"}
