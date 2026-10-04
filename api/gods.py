from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import get_db
from models.god import God
from schemas.god import GodCreate, GodResponse, GodUpdate

router = APIRouter(
    prefix="/gods",
    tags=["Gods"],
)


@router.get("", response_model=list[GodResponse])
def get_gods(db: Session = Depends(get_db)):
    return db.query(God).all()


@router.get("/{id}", response_model=GodResponse)
def get_god(id: int, db: Session = Depends(get_db)):
    god = db.query(God).filter(God.id == id).first()

    if not god:
        raise HTTPException(status_code=404, detail="Not found")

    return god


@router.post("", response_model=GodResponse)
def create_god(god: GodCreate, db: Session = Depends(get_db)):
    new_god = God(**god.model_dump())

    db.add(new_god)
    db.commit()
    db.refresh(new_god)

    return new_god


@router.put("/{id}", response_model=GodResponse)
def update_god(id: int, god: GodUpdate, db: Session = Depends(get_db)):
    existing = db.query(God).filter(God.id == id).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Not found")

    for field, value in god.model_dump(exclude_unset=True).items():
        setattr(existing, field, value)

    db.commit()
    db.refresh(existing)

    return existing


@router.delete("/{id}")
def delete_god(id: int, db: Session = Depends(get_db)):
    god = db.query(God).filter(God.id == id).first()

    if not god:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(god)
    db.commit()

    return {"message": "Deleted"}


@router.get("/{id}/children")
def get_god_children(id: int, db: Session = Depends(get_db)):
    god = db.query(God).filter(God.id == id).first()

    if not god:
        raise HTTPException(status_code=404, detail="Not found")

    return {
        "god": god.name,
        "children": god.children,
    }
