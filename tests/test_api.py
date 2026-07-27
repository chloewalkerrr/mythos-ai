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
        params={
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
        params={"status": "missing"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Updated"
    assert data["character"] == "Percy Jackson"
    assert data["new_status"] == "missing"


def test_update_missing_character_returns_404(client):
    response = client.put(
        "/characters/999",
        params={"status": "missing"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Not found"


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
