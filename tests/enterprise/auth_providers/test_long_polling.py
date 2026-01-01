"""Tests for enterprise.auth.providers.long_polling."""
    import pytest
    class TestLongPollingManager:
        def test_init(self):
            from enterprise.auth.providers.long_polling import LongPollingManager
            obj = LongPollingManager()
            assert obj is not None

        def test_not_configured_raises(self):
            from enterprise.auth.providers.long_polling import LongPollingManager
            obj = LongPollingManager()
            with pytest.raises(RuntimeError):
                obj.execute()

        def test_configure_and_validate(self):
            from enterprise.auth.providers.long_polling import LongPollingManager
            obj = LongPollingManager()
            obj.configure(key="value")
            assert obj.validate() is True

        def test_repr(self):
            from enterprise.auth.providers.long_polling import LongPollingManager
            obj = LongPollingManager()
            assert "LongPollingManager" in repr(obj)
