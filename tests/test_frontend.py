"""The Ask page shares the API origin without changing the API contract."""

import pytest


def test_ask_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert 'id="ask-form"' in response.text
    assert 'src="/assets/app.js"' in response.text
    assert 'href="/assets/styles.css"' in response.text


@pytest.mark.parametrize("asset", ["app.js", "styles.css"])
def test_frontend_assets(client, asset):
    response = client.get(f"/assets/{asset}")
    assert response.status_code == 200
    assert response.content


def test_static_routes_do_not_shadow_api(client):
    schema = client.get("/openapi.json").json()
    assert "post" in schema["paths"]["/ask"]
    assert "get" in schema["paths"]["/characters"]
    assert client.get("/assets/missing.js").status_code == 404
    assert client.get("/assets/.env").status_code == 404
