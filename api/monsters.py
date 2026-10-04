from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import get_db
from models.all_models import Monster
from schemas.monster import MonsterCreate, MonsterResponse, MonsterUpdate

router = APIRouter(
    prefix="/monsters",
    tags=["Monsters"],
)


@router.get("", response_model=list[MonsterResponse])
def get_monsters(db: Session = Depends(get_db)):
    return db.query(Monster).all()


@router.get("/{id}", response_model=MonsterResponse)
def get_monster(id: int, db: Session = Depends(get_db)):
    monster = db.query(Monster).filter(Monster.id == id).first()

    if not monster:
        raise HTTPException(status_code=404, detail="Not found")

    return monster


@router.post("", response_model=MonsterResponse)
def create_monster(monster: MonsterCreate, db: Session = Depends(get_db)):
    new_monster = Monster(**monster.model_dump())

    db.add(new_monster)
    db.commit()
    db.refresh(new_monster)

    return new_monster


@router.put("/{id}", response_model=MonsterResponse)
def update_monster(id: int, monster: MonsterUpdate, db: Session = Depends(get_db)):
    existing = db.query(Monster).filter(Monster.id == id).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Not found")

    for field, value in monster.model_dump(exclude_unset=True).items():
        setattr(existing, field, value)

    db.commit()
    db.refresh(existing)

    return existing


@router.delete("/{id}")
def delete_monster(id: int, db: Session = Depends(get_db)):
    monster = db.query(Monster).filter(Monster.id == id).first()

    if not monster:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(monster)
    db.commit()

    return {"message": "Deleted"}
