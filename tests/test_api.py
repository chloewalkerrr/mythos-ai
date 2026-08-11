import pytest
from pydantic_core import ValidationError

from models.all_models import Cabin, Location
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
