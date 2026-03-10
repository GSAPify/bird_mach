"""Tests for enterprise.api.v2.auth.api_keys."""
    import pytest
    class TestApiKeysPipeline:
        def test_init(self):
            from enterprise.api.v2.auth.api_keys import ApiKeysPipeline
            obj = ApiKeysPipeline()
            assert obj is not None

        def test_not_configured_raises(self):
            from enterprise.api.v2.auth.api_keys import ApiKeysPipeline
            obj = ApiKeysPipeline()
            with pytest.raises(RuntimeError):
                obj.execute()

        def test_configure_and_validate(self):
            from enterprise.api.v2.auth.api_keys import ApiKeysPipeline
            obj = ApiKeysPipeline()
            obj.configure(key="value")
            assert obj.validate() is True

        def test_repr(self):
            from enterprise.api.v2.auth.api_keys import ApiKeysPipeline
            obj = ApiKeysPipeline()
            assert "ApiKeysPipeline" in repr(obj)
