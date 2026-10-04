import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from api.main import app
from models import Base, get_db
from models.all_models import Book, CharacterPower, Power, Quest, QuestParticipant
from models.character import Character
from models.god import God

TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture()
def db_session():
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture()
def sample_data(db_session):
    poseidon = God(
        name="Poseidon",
        roman_name="Neptune",
        title="God of the Sea",
        domain="Sea",
    )

    db_session.add(poseidon)
    db_session.commit()
    db_session.refresh(poseidon)

    percy = Character(
        name="Percy Jackson",
        age=16,
        gender="Male",
        parent_god_id=poseidon.id,
        status="alive",
    )

    db_session.add(percy)
    db_session.commit()
    db_session.refresh(percy)

    hydrokinesis = Power(
        name="Hydrokinesis",
        description="Control over water",
        power_type="Elemental",
        power_level=10,
    )

    db_session.add(hydrokinesis)
    db_session.commit()
    db_session.refresh(hydrokinesis)

    character_power = CharacterPower(
        character_id=percy.id,
        power_id=hydrokinesis.id,
        proficiency_level=10,
    )

    db_session.add(character_power)
    db_session.commit()

    book = Book(
        title="The Lightning Thief",
        book_number=1,
        page_count=377,
    )

    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)

    quest = Quest(
        title="Retrieve Zeus's Master Bolt",
        description="Recover Zeus's stolen master bolt.",
        objective="Return the master bolt to Zeus.",
        status="completed",
        difficulty_level=8,
        book_id=book.id,
    )

    db_session.add(quest)
    db_session.commit()
    db_session.refresh(quest)

    participant = QuestParticipant(
        quest_id=quest.id,
        character_id=percy.id,
        role="Leader",
    )

    db_session.add(participant)
    db_session.commit()

    return {
        "poseidon": poseidon,
        "percy": percy,
        "hydrokinesis": hydrokinesis,
        "book": book,
        "quest": quest,
    }
