import pytest
from pydantic_core import ValidationError

from models.all_models import Book, Cabin, Location, Monster, Power, Prophecy, Weapon
from models.config import Settings


def test_openapi_docs_available(client):
    response = client.get("/docs")

    assert response.status_code == 200


def test_openapi_schema_available(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200

    data = response.json()

    assert "openapi" in data
    assert "paths" in data


def test_get_characters_returns_sample_character(client, sample_data):
    response = client.get("/characters")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Percy Jackson"
    assert data[0]["age"] == 16
    assert data[0]["status"] == "alive"


def test_get_character_by_id(client, sample_data):
    percy = sample_data["percy"]

    response = client.get(f"/characters/{percy.id}")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Percy Jackson"
    assert data["age"] == 16


def test_get_missing_character_returns_404(client):
    response = client.get("/characters/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_get_gods_returns_poseidon(client, sample_data):
    response = client.get("/gods")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Poseidon"


def test_create_character(client):
    response = client.post(
        "/characters",
        json={
            "name": "Annabeth Chase",
            "age": 16,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Created"
    assert data["character"] == "Annabeth Chase"


def test_update_character(client, sample_data):
    percy = sample_data["percy"]

    response = client.put(
        f"/characters/{percy.id}",
        json={"status": "missing"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Updated"
    assert data["character"] == "Percy Jackson"
    assert data["new_status"] == "missing"


def test_update_missing_character_returns_404(client):
    response = client.put(
        "/characters/999",
        json={"status": "missing"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_update_character_rejects_empty_status(client, sample_data):
    percy = sample_data["percy"]

    response = client.put(
        f"/characters/{percy.id}",
        json={"status": ""},
    )

    assert response.status_code == 422


def test_delete_character(client, sample_data):
    percy = sample_data["percy"]

    response = client.delete(f"/characters/{percy.id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Deleted"

    get_response = client.get(f"/characters/{percy.id}")

    assert get_response.status_code == 404


def test_delete_missing_character_returns_404(client):
    response = client.delete("/characters/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_get_god_children(client, sample_data):
    poseidon = sample_data["poseidon"]

    response = client.get(f"/gods/{poseidon.id}/children")

    assert response.status_code == 200

    data = response.json()

    assert data["god"] == "Poseidon"
    assert len(data["children"]) == 1
    assert data["children"][0]["name"] == "Percy Jackson"


def test_get_missing_god_children_returns_404(client):
    response = client.get("/gods/999/children")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_get_character_powers(client, sample_data):
    percy = sample_data["percy"]

    response = client.get(f"/characters/{percy.id}/powers")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["character"] == "Percy Jackson"
    assert data[0]["power"] == "Hydrokinesis"


def test_get_character_quests(client, sample_data):
    percy = sample_data["percy"]

    response = client.get(f"/characters/{percy.id}/quests")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["character"] == "Percy Jackson"
    assert data[0]["quest"] == "Retrieve Zeus's Master Bolt"
    assert data[0]["book"] == "The Lightning Thief"


def test_create_character_rejects_invalid_age(client):
    response = client.post(
        "/characters",
        json={
            "name": "Test Character",
            "age": -1,
        },
    )

    assert response.status_code == 422


def test_settings_require_db_user(monkeypatch):
    monkeypatch.delenv("DB_USER", raising=False)
    monkeypatch.delenv("DB_NAME", raising=False)
    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_get_god_by_id(client, sample_data):
    poseidon = sample_data["poseidon"]

    response = client.get(f"/gods/{poseidon.id}")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Poseidon"
    assert data["roman_name"] == "Neptune"


def test_get_missing_god_returns_404(client):
    response = client.get("/gods/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_create_god(client):
    response = client.post(
        "/gods",
        json={
            "name": "Athena",
            "domain": "Wisdom",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Athena"
    assert data["domain"] == "Wisdom"
    assert data["roman_name"] is None


def test_update_god(client, sample_data):
    poseidon = sample_data["poseidon"]

    response = client.put(
        f"/gods/{poseidon.id}",
        json={"title": "God of Earthquakes"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "God of Earthquakes"
    assert data["name"] == "Poseidon"


def test_update_missing_god_returns_404(client):
    response = client.put(
        "/gods/999",
        json={"title": "Nobody"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_delete_god(client, sample_data):
    poseidon = sample_data["poseidon"]

    response = client.delete(f"/gods/{poseidon.id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Deleted"

    get_response = client.get(f"/gods/{poseidon.id}")

    assert get_response.status_code == 404


def test_delete_missing_god_returns_404(client):
    response = client.delete("/gods/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_create_cabin(client, sample_data):
    poseidon = sample_data["poseidon"]

    response = client.post(
        "/cabins",
        json={
            "cabin_number": 3,
            "patron_god_id": poseidon.id,
            "color_scheme": "Blue and Green",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["cabin_number"] == 3
    assert data["patron_god_id"] == poseidon.id
    assert data["color_scheme"] == "Blue and Green"


def test_get_cabin_by_id(client, sample_data, db_session):
    poseidon = sample_data["poseidon"]

    cabin = Cabin(cabin_number=3, patron_god_id=poseidon.id, color_scheme="Blue")

    db_session.add(cabin)
    db_session.commit()
    db_session.refresh(cabin)

    response = client.get(f"/cabins/{cabin.id}")

    assert response.status_code == 200

    data = response.json()

    assert data["cabin_number"] == 3
    assert data["color_scheme"] == "Blue"


def test_get_missing_cabin_returns_404(client):
    response = client.get("/cabins/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_update_cabin(client, sample_data, db_session):
    poseidon = sample_data["poseidon"]

    cabin = Cabin(cabin_number=5, patron_god_id=poseidon.id, color_scheme="Red")

    db_session.add(cabin)
    db_session.commit()
    db_session.refresh(cabin)

    response = client.put(
        f"/cabins/{cabin.id}",
        json={"color_scheme": "Gold"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["color_scheme"] == "Gold"
    assert data["cabin_number"] == 5


def test_update_missing_cabin_returns_404(client):
    response = client.put(
        "/cabins/999",
        json={"color_scheme": "Gold"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_delete_cabin(client, sample_data, db_session):
    poseidon = sample_data["poseidon"]

    cabin = Cabin(cabin_number=7, patron_god_id=poseidon.id)

    db_session.add(cabin)
    db_session.commit()
    db_session.refresh(cabin)

    response = client.delete(f"/cabins/{cabin.id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Deleted"

    get_response = client.get(f"/cabins/{cabin.id}")

    assert get_response.status_code == 404


def test_delete_missing_cabin_returns_404(client):
    response = client.delete("/cabins/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_get_cabins_returns_created_cabin(client, sample_data, db_session):
    poseidon = sample_data["poseidon"]

    cabin = Cabin(cabin_number=9, patron_god_id=poseidon.id)

    db_session.add(cabin)
    db_session.commit()
    db_session.refresh(cabin)

    response = client.get("/cabins")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["cabin_number"] == 9


def test_get_locations_returns_created_location(client, db_session):
    location = Location(name="Camp Half-Blood", realm="Mortal")

    db_session.add(location)
    db_session.commit()
    db_session.refresh(location)

    response = client.get("/locations")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Camp Half-Blood"


def test_get_location_by_id(client, db_session):
    location = Location(name="Mount Olympus", realm="Olympus")

    db_session.add(location)
    db_session.commit()
    db_session.refresh(location)

    response = client.get(f"/locations/{location.id}")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Mount Olympus"
    assert data["realm"] == "Olympus"


def test_get_missing_location_returns_404(client):
    response = client.get("/locations/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_create_location(client):
    response = client.post(
        "/locations",
        json={
            "name": "Underworld",
            "location_type": "Divine Realm",
            "realm": "Underworld",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Underworld"
    assert data["location_type"] == "Divine Realm"
    assert data["coordinates"] is None


def test_update_location(client, db_session):
    location = Location(name="Lotus Hotel", realm="Mortal")

    db_session.add(location)
    db_session.commit()
    db_session.refresh(location)

    response = client.put(
        f"/locations/{location.id}",
        json={"description": "A magical casino"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["description"] == "A magical casino"
    assert data["name"] == "Lotus Hotel"


def test_update_missing_location_returns_404(client):
    response = client.put(
        "/locations/999",
        json={"description": "Nowhere"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_delete_location(client, db_session):
    location = Location(name="Camp Jupiter", realm="Mortal")

    db_session.add(location)
    db_session.commit()
    db_session.refresh(location)

    response = client.delete(f"/locations/{location.id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Deleted"

    get_response = client.get(f"/locations/{location.id}")

    assert get_response.status_code == 404


def test_delete_missing_location_returns_404(client):
    response = client.delete("/locations/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_get_monsters_returns_created_monster(client, db_session):
    monster = Monster(name="Medusa", threat_level="extreme")

    db_session.add(monster)
    db_session.commit()
    db_session.refresh(monster)

    response = client.get("/monsters")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Medusa"


def test_get_monster_by_id(client, db_session):
    monster = Monster(name="Chimera", threat_level="extreme")

    db_session.add(monster)
    db_session.commit()
    db_session.refresh(monster)

    response = client.get(f"/monsters/{monster.id}")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Chimera"
    assert data["threat_level"] == "extreme"


def test_get_missing_monster_returns_404(client):
    response = client.get("/monsters/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_create_monster(client):
    response = client.post(
        "/monsters",
        json={
            "name": "Hellhound",
            "threat_level": "high",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Hellhound"
    assert data["threat_level"] == "high"


def test_create_monster_rejects_invalid_threat_level(client):
    response = client.post(
        "/monsters",
        json={
            "name": "Mystery Beast",
            "threat_level": "catastrophic",
        },
    )

    assert response.status_code == 422


def test_update_monster(client, db_session):
    monster = Monster(name="Minotaur", threat_level="high")

    db_session.add(monster)
    db_session.commit()
    db_session.refresh(monster)

    response = client.put(
        f"/monsters/{monster.id}",
        json={"threat_level": "extreme"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["threat_level"] == "extreme"
    assert data["name"] == "Minotaur"


def test_update_missing_monster_returns_404(client):
    response = client.put(
        "/monsters/999",
        json={"threat_level": "low"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_delete_monster(client, db_session):
    monster = Monster(name="Cerberus", threat_level="extreme")

    db_session.add(monster)
    db_session.commit()
    db_session.refresh(monster)

    response = client.delete(f"/monsters/{monster.id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Deleted"

    get_response = client.get(f"/monsters/{monster.id}")

    assert get_response.status_code == 404


def test_delete_missing_monster_returns_404(client):
    response = client.delete("/monsters/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_get_weapons_returns_created_weapon(client, db_session):
    weapon = Weapon(name="Riptide", weapon_type="Sword")

    db_session.add(weapon)
    db_session.commit()
    db_session.refresh(weapon)

    response = client.get("/weapons")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Riptide"


def test_get_weapon_by_id(client, db_session):
    weapon = Weapon(name="Backbiter", weapon_type="Sword")

    db_session.add(weapon)
    db_session.commit()
    db_session.refresh(weapon)

    response = client.get(f"/weapons/{weapon.id}")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Backbiter"


def test_get_missing_weapon_returns_404(client):
    response = client.get("/weapons/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_create_weapon(client, sample_data):
    percy = sample_data["percy"]

    response = client.post(
        "/weapons",
        json={
            "name": "Anaklusmos",
            "weapon_type": "Sword",
            "owner_id": percy.id,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Anaklusmos"
    assert data["owner_id"] == percy.id


def test_update_weapon(client, db_session):
    weapon = Weapon(name="Dagger", weapon_type="Dagger")

    db_session.add(weapon)
    db_session.commit()
    db_session.refresh(weapon)

    response = client.put(
        f"/weapons/{weapon.id}",
        json={"material": "Celestial Bronze"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["material"] == "Celestial Bronze"
    assert data["name"] == "Dagger"


def test_update_missing_weapon_returns_404(client):
    response = client.put(
        "/weapons/999",
        json={"material": "Gold"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_delete_weapon(client, db_session):
    weapon = Weapon(name="Spear", weapon_type="Spear")

    db_session.add(weapon)
    db_session.commit()
    db_session.refresh(weapon)

    response = client.delete(f"/weapons/{weapon.id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Deleted"

    get_response = client.get(f"/weapons/{weapon.id}")

    assert get_response.status_code == 404


def test_delete_missing_weapon_returns_404(client):
    response = client.delete("/weapons/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_get_powers_returns_created_power(client, db_session):
    power = Power(name="Telekinesis", power_level=7)

    db_session.add(power)
    db_session.commit()
    db_session.refresh(power)

    response = client.get("/powers")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Telekinesis"


def test_get_power_by_id(client, db_session):
    power = Power(name="Shapeshifting", power_level=6)

    db_session.add(power)
    db_session.commit()
    db_session.refresh(power)

    response = client.get(f"/powers/{power.id}")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Shapeshifting"
    assert data["power_level"] == 6


def test_get_missing_power_returns_404(client):
    response = client.get("/powers/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_create_power(client):
    response = client.post(
        "/powers",
        json={
            "name": "Fire Breathing",
            "power_level": 8,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Fire Breathing"
    assert data["power_level"] == 8


def test_create_power_rejects_invalid_power_level(client):
    response = client.post(
        "/powers",
        json={
            "name": "Too Strong",
            "power_level": 11,
        },
    )

    assert response.status_code == 422


def test_update_power(client, db_session):
    power = Power(name="Mind Reading", power_level=5)

    db_session.add(power)
    db_session.commit()
    db_session.refresh(power)

    response = client.put(
        f"/powers/{power.id}",
        json={"power_level": 9},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["power_level"] == 9
    assert data["name"] == "Mind Reading"


def test_update_missing_power_returns_404(client):
    response = client.put(
        "/powers/999",
        json={"power_level": 3},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_delete_power(client, db_session):
    power = Power(name="Invisibility", power_level=6)

    db_session.add(power)
    db_session.commit()
    db_session.refresh(power)

    response = client.delete(f"/powers/{power.id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Deleted"

    get_response = client.get(f"/powers/{power.id}")

    assert get_response.status_code == 404


def test_delete_missing_power_returns_404(client):
    response = client.delete("/powers/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_get_books_returns_created_book(client, db_session):
    book = Book(title="The Sea of Monsters", book_number=2, page_count=279)

    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)

    response = client.get("/books")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "The Sea of Monsters"


def test_get_book_by_id(client, db_session):
    book = Book(title="The Titan's Curse", book_number=3, page_count=312)

    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)

    response = client.get(f"/books/{book.id}")

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "The Titan's Curse"
    assert data["book_number"] == 3


def test_get_missing_book_returns_404(client):
    response = client.get("/books/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_create_book(client):
    response = client.post(
        "/books",
        json={
            "title": "The Battle of the Labyrinth",
            "book_number": 4,
            "page_count": 361,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "The Battle of the Labyrinth"
    assert data["book_number"] == 4


def test_create_book_rejects_invalid_page_count(client):
    response = client.post(
        "/books",
        json={
            "title": "Broken Book",
            "book_number": 6,
            "page_count": 0,
        },
    )

    assert response.status_code == 422


def test_create_book_rejects_invalid_book_number(client):
    response = client.post(
        "/books",
        json={
            "title": "Zero Book",
            "book_number": 0,
        },
    )

    assert response.status_code == 422


def test_update_book(client, db_session):
    book = Book(title="The Last Olympian", book_number=5, page_count=381)

    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)

    response = client.put(
        f"/books/{book.id}",
        json={"summary": "The final battle for Olympus."},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["summary"] == "The final battle for Olympus."
    assert data["title"] == "The Last Olympian"


def test_update_missing_book_returns_404(client):
    response = client.put(
        "/books/999",
        json={"summary": "Nowhere"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_delete_book(client, db_session):
    book = Book(title="Test Book", book_number=99, page_count=100)

    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)

    response = client.delete(f"/books/{book.id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Deleted"

    get_response = client.get(f"/books/{book.id}")

    assert get_response.status_code == 404


def test_delete_missing_book_returns_404(client):
    response = client.delete("/books/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_get_prophecies_returns_created_prophecy(client, db_session):
    prophecy = Prophecy(text="A hero's soul, cursed blade shall reap.")

    db_session.add(prophecy)
    db_session.commit()
    db_session.refresh(prophecy)

    response = client.get("/prophecies")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["text"] == "A hero's soul, cursed blade shall reap."


def test_get_prophecy_by_id(client, db_session):
    prophecy = Prophecy(text="Olympus to preserve or raze.", speaker="The Oracle")

    db_session.add(prophecy)
    db_session.commit()
    db_session.refresh(prophecy)

    response = client.get(f"/prophecies/{prophecy.id}")

    assert response.status_code == 200

    data = response.json()

    assert data["speaker"] == "The Oracle"


def test_get_missing_prophecy_returns_404(client):
    response = client.get("/prophecies/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_create_prophecy(client):
    response = client.post(
        "/prophecies",
        json={
            "text": "A test prophecy of great importance.",
            "speaker": "The Oracle",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["text"] == "A test prophecy of great importance."
    assert data["fulfilled"] is False


def test_update_prophecy(client, db_session):
    prophecy = Prophecy(text="An old prophecy.", fulfilled=False)

    db_session.add(prophecy)
    db_session.commit()
    db_session.refresh(prophecy)

    response = client.put(
        f"/prophecies/{prophecy.id}",
        json={"fulfilled": True},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["fulfilled"] is True
    assert data["text"] == "An old prophecy."


def test_update_missing_prophecy_returns_404(client):
    response = client.put(
        "/prophecies/999",
        json={"fulfilled": True},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


def test_delete_prophecy(client, db_session):
    prophecy = Prophecy(text="A prophecy to be deleted.")

    db_session.add(prophecy)
    db_session.commit()
    db_session.refresh(prophecy)

    response = client.delete(f"/prophecies/{prophecy.id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Deleted"

    get_response = client.get(f"/prophecies/{prophecy.id}")

    assert get_response.status_code == 404


def test_delete_missing_prophecy_returns_404(client):
    response = client.delete("/prophecies/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"
