"""Tests for enterprise.streaming.hook_registry."""
    import pytest
    class TestHookRegistryBuilder:
        def test_init(self):
            from enterprise.streaming.hook_registry import HookRegistryBuilder
            obj = HookRegistryBuilder()
            assert obj is not None

        def test_not_configured_raises(self):
            from enterprise.streaming.hook_registry import HookRegistryBuilder
            obj = HookRegistryBuilder()
            with pytest.raises(RuntimeError):
                obj.execute()

        def test_configure_and_validate(self):
            from enterprise.streaming.hook_registry import HookRegistryBuilder
            obj = HookRegistryBuilder()
            obj.configure(key="value")
            assert obj.validate() is True

        def test_repr(self):
            from enterprise.streaming.hook_registry import HookRegistryBuilder
            obj = HookRegistryBuilder()
            assert "HookRegistryBuilder" in repr(obj)
