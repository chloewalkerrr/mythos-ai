from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import get_db
from models.character import Character
from schemas.character import CharacterCreate, CharacterResponse, CharacterUpdate

router = APIRouter(
    prefix="/characters",
    tags=["Characters"],
)


@router.get(
    "",
    response_model=list[CharacterResponse],
)
def get_characters(db: Session = Depends(get_db)):
    return db.query(Character).all()


@router.get(
    "/{id}",
    response_model=CharacterResponse,
)
def get_character(id: int, db: Session = Depends(get_db)):
    char = db.query(Character).filter(Character.id == id).first()

    if not char:
        raise HTTPException(status_code=404, detail="Not found")

    return char


@router.post("")
def create_character(
    character: CharacterCreate,
    db: Session = Depends(get_db),
):
    new_char = Character(
        name=character.name,
        age=character.age,
    )

    db.add(new_char)
    db.commit()
    db.refresh(new_char)

    return {
        "message": "Created",
        "character": new_char.name,
    }


@router.put("/{id}")
def update_character(
    id: int,
    character: CharacterUpdate,
    db: Session = Depends(get_db),
):
    char = db.query(Character).filter(Character.id == id).first()

    if not char:
        raise HTTPException(status_code=404, detail="Not found")

    char.status = character.status
    db.commit()
    db.refresh(char)

    return {
        "message": "Updated",
        "character": char.name,
        "new_status": char.status,
    }


@router.delete("/{id}")
def delete_character(id: int, db: Session = Depends(get_db)):
    char = db.query(Character).filter(Character.id == id).first()

    if not char:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(char)
    db.commit()

    return {"message": "Deleted"}
