from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import get_db
from models.god import God

router = APIRouter(
    prefix="/gods",
    tags=["Gods"],
)


@router.get("")
def get_gods(db: Session = Depends(get_db)):
    return db.query(God).all()


@router.get("/{id}/children")
def get_god_children(id: int, db: Session = Depends(get_db)):
    god = db.query(God).filter(God.id == id).first()

    if not god:
        raise HTTPException(status_code=404, detail="Not found")

    return {
        "god": god.name,
        "children": god.children,
    }
