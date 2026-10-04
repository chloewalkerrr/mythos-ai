from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import get_db
from models.all_models import Power
from schemas.power import PowerCreate, PowerResponse, PowerUpdate

router = APIRouter(
    prefix="/powers",
    tags=["Powers"],
)


@router.get("", response_model=list[PowerResponse])
def get_powers(db: Session = Depends(get_db)):
    return db.query(Power).all()


@router.get("/{id}", response_model=PowerResponse)
def get_power(id: int, db: Session = Depends(get_db)):
    power = db.query(Power).filter(Power.id == id).first()

    if not power:
        raise HTTPException(status_code=404, detail="Not found")

    return power


@router.post("", response_model=PowerResponse)
def create_power(power: PowerCreate, db: Session = Depends(get_db)):
    new_power = Power(**power.model_dump())

    db.add(new_power)
    db.commit()
    db.refresh(new_power)

    return new_power


@router.put("/{id}", response_model=PowerResponse)
def update_power(id: int, power: PowerUpdate, db: Session = Depends(get_db)):
    existing = db.query(Power).filter(Power.id == id).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Not found")

    for field, value in power.model_dump(exclude_unset=True).items():
        setattr(existing, field, value)

    db.commit()
    db.refresh(existing)

    return existing


@router.delete("/{id}")
def delete_power(id: int, db: Session = Depends(get_db)):
    power = db.query(Power).filter(Power.id == id).first()

    if not power:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(power)
    db.commit()

    return {"message": "Deleted"}
