from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import get_db
from models.all_models import Weapon
from schemas.weapon import WeaponCreate, WeaponResponse, WeaponUpdate

router = APIRouter(
    prefix="/weapons",
    tags=["Weapons"],
)


@router.get("", response_model=list[WeaponResponse])
def get_weapons(db: Session = Depends(get_db)):
    return db.query(Weapon).all()


@router.get("/{id}", response_model=WeaponResponse)
def get_weapon(id: int, db: Session = Depends(get_db)):
    weapon = db.query(Weapon).filter(Weapon.id == id).first()

    if not weapon:
        raise HTTPException(status_code=404, detail="Not found")

    return weapon


@router.post("", response_model=WeaponResponse)
def create_weapon(weapon: WeaponCreate, db: Session = Depends(get_db)):
    new_weapon = Weapon(**weapon.model_dump())

    db.add(new_weapon)
    db.commit()
    db.refresh(new_weapon)

    return new_weapon


@router.put("/{id}", response_model=WeaponResponse)
def update_weapon(id: int, weapon: WeaponUpdate, db: Session = Depends(get_db)):
    existing = db.query(Weapon).filter(Weapon.id == id).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Not found")

    for field, value in weapon.model_dump(exclude_unset=True).items():
        setattr(existing, field, value)

    db.commit()
    db.refresh(existing)

    return existing


@router.delete("/{id}")
def delete_weapon(id: int, db: Session = Depends(get_db)):
    weapon = db.query(Weapon).filter(Weapon.id == id).first()

    if not weapon:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(weapon)
    db.commit()

    return {"message": "Deleted"}
