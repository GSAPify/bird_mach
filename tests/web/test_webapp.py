from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from bird_mach.web.audio_fetch import fetch_audio_from_url
from bird_mach.webapp import app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


def test_health_endpoint(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "Mach"
    assert response.json()["version"]
    assert response.json()["max_upload_mb"] == 50


def test_home_page_links_static_assets(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert 'href="/static/css/theme.css"' in response.text
    assert 'src="/static/js/index.js"' in response.text
    assert 'action="/visualize"' in response.text
    assert "up to 50 MB" in response.text
    assert "aac, flac, m4a, mp3, ogg, wav" in response.text


def test_live_page_has_browser_audio_controls(client: TestClient) -> None:
    response = client.get("/live")

    assert response.status_code == 200
    assert 'id="startFileBtn"' in response.text
    assert 'id="startMicBtn"' in response.text
    assert 'id="startScreenBtn"' in response.text
    assert 'src="/static/js/live.js"' in response.text


def test_live_static_script_contains_audio_lifecycle_guards(client: TestClient) -> None:
    response = client.get("/static/js/live.js")

    assert response.status_code == 200
    assert "createMediaElementSource" in response.text
    assert "player.addEventListener(\"play\"" in response.text
    assert "disconnectCurrentSource" in response.text


def test_visualize_rejects_empty_submission(client: TestClient) -> None:
    response = client.post("/visualize", data={})

    assert response.status_code == 400
    assert "No audio received" in response.text


def test_favicon_is_served(client: TestClient) -> None:
    response = client.get("/static/img/favicon.svg")

    assert response.status_code == 200
    assert "<svg" in response.text


def test_fetch_audio_rejects_non_http_urls() -> None:
    with pytest.raises(ValueError, match="Only http/https URLs"):
        fetch_audio_from_url("file:///tmp/audio.wav")
