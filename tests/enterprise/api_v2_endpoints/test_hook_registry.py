"""Tests for enterprise.api.v2.endpoints.hook_registry."""
    import pytest
    class TestHookRegistryRepository:
        def test_init(self):
            from enterprise.api.v2.endpoints.hook_registry import HookRegistryRepository
            obj = HookRegistryRepository()
            assert obj is not None

        def test_not_configured_raises(self):
            from enterprise.api.v2.endpoints.hook_registry import HookRegistryRepository
            obj = HookRegistryRepository()
            with pytest.raises(RuntimeError):
                obj.execute()

        def test_configure_and_validate(self):
            from enterprise.api.v2.endpoints.hook_registry import HookRegistryRepository
            obj = HookRegistryRepository()
            obj.configure(key="value")
            assert obj.validate() is True

        def test_repr(self):
            from enterprise.api.v2.endpoints.hook_registry import HookRegistryRepository
            obj = HookRegistryRepository()
            assert "HookRegistryRepository" in repr(obj)
