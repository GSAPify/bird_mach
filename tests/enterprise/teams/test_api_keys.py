"""Tests for enterprise.teams.api_keys."""
    import pytest
    class TestApiKeysManager:
        def test_init(self):
            from enterprise.teams.api_keys import ApiKeysManager
            obj = ApiKeysManager()
            assert obj is not None

        def test_not_configured_raises(self):
            from enterprise.teams.api_keys import ApiKeysManager
            obj = ApiKeysManager()
            with pytest.raises(RuntimeError):
                obj.execute()

        def test_configure_and_validate(self):
            from enterprise.teams.api_keys import ApiKeysManager
            obj = ApiKeysManager()
            obj.configure(key="value")
            assert obj.validate() is True

        def test_repr(self):
            from enterprise.teams.api_keys import ApiKeysManager
            obj = ApiKeysManager()
            assert "ApiKeysManager" in repr(obj)
