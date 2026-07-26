import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from api.main import app
from models import Base, get_db
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

    return {
        "poseidon": poseidon,
        "percy": percy,
    }
