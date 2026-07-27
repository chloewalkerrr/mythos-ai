from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models import get_db
from models.all_models import Quest

router = APIRouter(
    prefix="/quests",
    tags=["Quests"],
)


@router.get("")
def get_quests(db: Session = Depends(get_db)):
    return db.query(Quest).all()
