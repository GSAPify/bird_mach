"""Tests for enterprise.api.v2.endpoints.local_storage."""
    import pytest
    class TestLocalStorageFactory:
        def test_init(self):
            from enterprise.api.v2.endpoints.local_storage import LocalStorageFactory
            obj = LocalStorageFactory()
            assert obj is not None

        def test_not_configured_raises(self):
            from enterprise.api.v2.endpoints.local_storage import LocalStorageFactory
            obj = LocalStorageFactory()
            with pytest.raises(RuntimeError):
                obj.execute()

        def test_configure_and_validate(self):
            from enterprise.api.v2.endpoints.local_storage import LocalStorageFactory
            obj = LocalStorageFactory()
            obj.configure(key="value")
            assert obj.validate() is True

        def test_repr(self):
            from enterprise.api.v2.endpoints.local_storage import LocalStorageFactory
            obj = LocalStorageFactory()
            assert "LocalStorageFactory" in repr(obj)
