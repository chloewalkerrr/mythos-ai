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
