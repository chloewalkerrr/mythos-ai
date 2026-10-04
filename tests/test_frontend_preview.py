"""The development-only preview server returns each mocked UI state."""

import pytest
from fastapi.testclient import TestClient

from scripts.preview_frontend import app


@pytest.mark.parametrize(
    ("state", "status", "insufficient"),
    [
        ("success", 200, False),
        ("insufficient", 200, True),
        ("error", 503, None),
        ("timeout", 504, None),
    ],
)
def test_preview_states(state, status, insufficient):
    with TestClient(app) as client:
        assert client.get("/").status_code == 200
        response = client.post(
            "/ask",
            json={"question": "Who is Percy?"},
            headers={"Referer": f"http://127.0.0.1:8001/?state={state}"},
        )
    assert response.status_code == status
    if insufficient is not None:
        assert response.json()["insufficient_context"] is insufficient
    if state == "success":
        assert response.json()["answer"].startswith("MOCK PREVIEW:")
        evidence = response.json()["evidence"][0]
        assert evidence["provenance"] == "attributed_summary"
        assert evidence["source_url"] == "https://rickriordan.com/character/percy-jackson/"
        assert evidence["reference"].startswith("Mock preview")
