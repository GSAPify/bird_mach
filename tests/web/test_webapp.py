from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from bird_mach.web.audio_fetch import fetch_audio_from_url
from bird_mach.web.routes import embedding_section_title, visualization_error
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


def test_security_headers_are_set(client: TestClient) -> None:
    response = client.get("/")

    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"
    assert response.headers["X-Frame-Options"] == "DENY"


def test_home_page_links_static_assets(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert 'href="/static/css/theme.css"' in response.text
    assert 'src="/static/js/index.js"' in response.text
    assert 'action="/visualize"' in response.text
    assert "up to 50 MB" in response.text
    assert "aac, flac, m4a, mp3, ogg, wav" in response.text


def test_home_page_includes_skip_link_and_landmarks(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert 'class="skip-link"' in response.text
    assert 'href="#main-content"' in response.text
    assert 'id="main-content"' in response.text
    assert 'aria-label="Primary"' in response.text


def test_home_page_includes_open_graph_meta(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert 'property="og:type"' in response.text
    assert 'property="og:title"' in response.text
    assert 'name="twitter:card"' in response.text


def test_home_page_links_configured_live_site(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("RENDER_EXTERNAL_URL", "https://bird-mach.onrender.com/")

    response = client.get("/")

    assert response.status_code == 200
    assert 'href="https://bird-mach.onrender.com"' in response.text
    assert "live site" in response.text


def test_live_page_has_browser_audio_controls(client: TestClient) -> None:
    response = client.get("/live")

    assert response.status_code == 200
    assert 'id="startFileBtn"' in response.text
    assert 'id="checkMicBtn"' in response.text
    assert 'id="startMicBtn"' in response.text
    assert 'id="startScreenBtn"' in response.text
    assert 'id="micDevice"' in response.text
    assert 'id="micPermission"' in response.text
    assert 'src="/static/js/live.js"' in response.text


def test_live_page_announces_status_and_compact_button(client: TestClient) -> None:
    response = client.get("/live")

    assert response.status_code == 200
    assert 'role="status"' in response.text
    assert 'aria-live="polite"' in response.text
    assert "btn-compact" in response.text


def test_live_static_script_contains_audio_lifecycle_guards(client: TestClient) -> None:
    response = client.get("/static/js/live.js")

    assert response.status_code == 200
    assert "createMediaElementSource" in response.text
    assert "player.addEventListener(\"play\"" in response.text
    assert "disconnectCurrentSource" in response.text
    assert "navigator.permissions.query" in response.text
    assert "enumerateDevices" in response.text
    assert "micAudioConstraints" in response.text


def test_upload_static_script_contains_preflight_guards(client: TestClient) -> None:
    response = client.get("/static/js/index.js")

    assert response.status_code == 200
    assert "maxUploadMb" in response.text
    assert "supportedFormats" in response.text
    assert "is-invalid" in response.text


def test_embedding_section_title_matches_dimension() -> None:
    assert embedding_section_title(use_2d=True) == "2D embedding (UMAP)"
    assert embedding_section_title(use_2d=False) == "3D embedding (UMAP)"


def test_visualization_error_escapes_html() -> None:
    response = visualization_error("<script>alert(1)</script>")

    assert response.status_code == 400
    body = bytes(response.body).decode("utf-8")
    assert "<script>" not in body
    assert "&lt;script&gt;" in body


def test_visualize_rejects_empty_submission(client: TestClient) -> None:
    response = client.post("/visualize", data={})

    assert response.status_code == 400
    assert "No audio received" in response.text


def test_visualize_rejects_unsupported_upload_extension(client: TestClient) -> None:
    response = client.post(
        "/visualize",
        files={"audio": ("notes.txt", b"not audio", "text/plain")},
    )

    assert response.status_code == 400
    assert "Unsupported audio format" in response.text


def test_visualize_rejects_oversized_upload(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("MAX_UPLOAD_MB", "1")
    payload = b"0" * (1024 * 1024 + 1)

    response = client.post(
        "/visualize",
        files={"audio": ("large.wav", payload, "audio/wav")},
    )

    assert response.status_code == 413
    assert "exceeds the 1 MB limit" in response.text


def test_favicon_is_served(client: TestClient) -> None:
    response = client.get("/static/img/favicon.svg")

    assert response.status_code == 200
    assert "<svg" in response.text


def test_fetch_audio_rejects_non_http_urls() -> None:
    with pytest.raises(ValueError, match="Only http/https URLs"):
        fetch_audio_from_url("file:///tmp/audio.wav")
