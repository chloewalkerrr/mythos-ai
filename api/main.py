"""
Percy Jackson Database API
Chloe Walker - CMSC 4323
"""

import sys

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

sys.path.append("..")

from api.characters import router as characters_router
from api.gods import router as gods_router
from api.quests import router as quests_router
from models import get_db
from models.all_models import Book, CharacterPower, Power, Quest, QuestParticipant
from models.character import Character

app = FastAPI(title="Percy Jackson Database")

app.include_router(characters_router)
app.include_router(gods_router)
app.include_router(quests_router)


# character's quests (multiple join)
@app.get("/characters/{id}/quests", tags=["Joins"])
def get_character_quests(id: int, db: Session = Depends(get_db)):
    # joins characters -> quest_participants -> quests -> books
    result = (
        db.query(Character.name, Quest.title, Book.title.label("book"))
        .join(QuestParticipant, Character.id == QuestParticipant.character_id)
        .join(Quest, QuestParticipant.quest_id == Quest.id)
        .join(Book, Quest.book_id == Book.id)
        .filter(Character.id == id)
        .all()
    )

    return [{"character": r[0], "quest": r[1], "book": r[2]} for r in result]


# character's powers (join query)
@app.get("/characters/{id}/powers", tags=["Joins"])
def get_character_powers(id: int, db: Session = Depends(get_db)):
    result = (
        db.query(Character.name, Power.name)
        .join(CharacterPower, Character.id == CharacterPower.character_id)
        .join(Power, CharacterPower.power_id == Power.id)
        .filter(Character.id == id)
        .all()
    )

    return [{"character": r[0], "power": r[1]} for r in result]


# view
@app.get("/views/character-summary", tags=["Views"])
def view_character_summary(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM character_power_summary")).fetchall()
    return [dict(row._mapping) for row in result]


# stored procedure
@app.get("/procedures/god-children/{god_name}", tags=["Procedures"])
def procedure_god_children(god_name: str, db: Session = Depends(get_db)):
    result = db.execute(text(f"CALL GetCharactersByGodParent('{god_name}')")).fetchall()
    return [dict(row._mapping) for row in result]
