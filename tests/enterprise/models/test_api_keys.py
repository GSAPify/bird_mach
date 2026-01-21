"""Tests for enterprise.models.api_keys."""
    import pytest
    class TestApiKeysObserver:
        def test_init(self):
            from enterprise.models.api_keys import ApiKeysObserver
            obj = ApiKeysObserver()
            assert obj is not None

        def test_not_configured_raises(self):
            from enterprise.models.api_keys import ApiKeysObserver
            obj = ApiKeysObserver()
            with pytest.raises(RuntimeError):
                obj.execute()

        def test_configure_and_validate(self):
            from enterprise.models.api_keys import ApiKeysObserver
            obj = ApiKeysObserver()
            obj.configure(key="value")
            assert obj.validate() is True

        def test_repr(self):
            from enterprise.models.api_keys import ApiKeysObserver
            obj = ApiKeysObserver()
            assert "ApiKeysObserver" in repr(obj)
