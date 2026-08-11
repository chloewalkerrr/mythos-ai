from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import get_db
from models.all_models import Prophecy
from schemas.prophecy import ProphecyCreate, ProphecyResponse, ProphecyUpdate

router = APIRouter(
    prefix="/prophecies",
    tags=["Prophecies"],
)


@router.get("", response_model=list[ProphecyResponse])
def get_prophecies(db: Session = Depends(get_db)):
    return db.query(Prophecy).all()


@router.get("/{id}", response_model=ProphecyResponse)
def get_prophecy(id: int, db: Session = Depends(get_db)):
    prophecy = db.query(Prophecy).filter(Prophecy.id == id).first()

    if not prophecy:
        raise HTTPException(status_code=404, detail="Not found")

    return prophecy


@router.post("", response_model=ProphecyResponse)
def create_prophecy(prophecy: ProphecyCreate, db: Session = Depends(get_db)):
    new_prophecy = Prophecy(**prophecy.model_dump())

    db.add(new_prophecy)
    db.commit()
    db.refresh(new_prophecy)

    return new_prophecy


@router.put("/{id}", response_model=ProphecyResponse)
def update_prophecy(id: int, prophecy: ProphecyUpdate, db: Session = Depends(get_db)):
    existing = db.query(Prophecy).filter(Prophecy.id == id).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Not found")

    for field, value in prophecy.model_dump(exclude_unset=True).items():
        setattr(existing, field, value)

    db.commit()
    db.refresh(existing)

    return existing


@router.delete("/{id}")
def delete_prophecy(id: int, db: Session = Depends(get_db)):
    prophecy = db.query(Prophecy).filter(Prophecy.id == id).first()

    if not prophecy:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(prophecy)
    db.commit()

    return {"message": "Deleted"}
