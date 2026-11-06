"""Tests for webhook dispatcher."""
from bird_mach.webhooks.dispatcher import WebhookDispatcher, WebhookEvent

class TestWebhookDispatcher:
    def test_register(self):
        d = WebhookDispatcher()
        d.register("https://example.com/hook", "secret123")
        assert d.endpoint_count == 1

    def test_dispatch(self):
        d = WebhookDispatcher()
        d.register("https://example.com/hook", "secret", {"analysis.complete"})
        event = WebhookEvent("analysis.complete", {"id": "123"})
        assert d.dispatch(event) == 1

    def test_filter_events(self):
        d = WebhookDispatcher()
        d.register("https://example.com/hook", "s", {"upload"})
        event = WebhookEvent("analysis.complete", {})
        assert d.dispatch(event) == 0

    def test_unregister(self):
        d = WebhookDispatcher()
        d.register("https://example.com/hook", "s")
        assert d.unregister("https://example.com/hook")
        assert d.endpoint_count == 0

    def test_sign(self):
        event = WebhookEvent("test", {"key": "value"})
        sig = event.sign("secret")
        assert len(sig) == 64


def test_reregistering_url_does_not_double_deliver():
    from bird_mach.webhooks.dispatcher import WebhookDispatcher, WebhookEvent
    d = WebhookDispatcher()
    d.register("http://x", "old")
    ep = d.register("http://x", "new", events={"audio.uploaded"})
    assert ep.secret == "new"
    assert d.dispatch(WebhookEvent("audio.uploaded", {})) == 1
