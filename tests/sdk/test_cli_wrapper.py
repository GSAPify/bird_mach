"""Tests for the SDK CLI wrapper."""
import pytest

from bird_mach.sdk import cli_wrapper


class FakeClient:
    instances = []
    fail = False

    def __init__(self, config):
        self.config = config
        self.events = []
        FakeClient.instances.append(self)

    def connect(self):
        self.events.append("connect")

    def close(self):
        self.events.append("close")

    def analyze(self, path):
        self.events.append("analyze")
        if FakeClient.fail:
            raise RuntimeError("boom")
        return {"path": path}

    def search(self, query, limit=10):
        self.events.append("search")
        return [{"q": query, "limit": limit}]


@pytest.fixture(autouse=True)
def fake_client(monkeypatch):
    FakeClient.instances.clear()
    monkeypatch.setattr(FakeClient, "fail", False)
    monkeypatch.setattr(cli_wrapper, "MachClient", FakeClient)


def test_run_analyze_returns_result_and_closes_client():
    assert cli_wrapper.run_analyze("a.wav") == {"path": "a.wav"}
    assert FakeClient.instances[0].events == ["connect", "analyze", "close"]


def test_run_analyze_passes_config_to_client():
    cli_wrapper.run_analyze("a.wav", api_key="k", base_url="http://example.test")
    config = FakeClient.instances[0].config
    assert config.base_url == "http://example.test"
    assert config.api_key == "k"


def test_run_analyze_closes_client_when_analyze_fails(monkeypatch):
    monkeypatch.setattr(FakeClient, "fail", True)
    with pytest.raises(RuntimeError):
        cli_wrapper.run_analyze("a.wav")
    assert FakeClient.instances[0].events[-1] == "close"
