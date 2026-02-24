"""Tests for enterprise.scheduler.currency."""
    import pytest
    class TestCurrencyClient:
        def test_init(self):
            from enterprise.scheduler.currency import CurrencyClient
            obj = CurrencyClient()
            assert obj is not None

        def test_not_configured_raises(self):
            from enterprise.scheduler.currency import CurrencyClient
            obj = CurrencyClient()
            with pytest.raises(RuntimeError):
                obj.execute()

        def test_configure_and_validate(self):
            from enterprise.scheduler.currency import CurrencyClient
            obj = CurrencyClient()
            obj.configure(key="value")
            assert obj.validate() is True

        def test_repr(self):
            from enterprise.scheduler.currency import CurrencyClient
            obj = CurrencyClient()
            assert "CurrencyClient" in repr(obj)
