"""Tests for enterprise.api.v2.gcs_storage."""
    import pytest
    class TestGcsStorageSerializer:
        def test_init(self):
            from enterprise.api.v2.gcs_storage import GcsStorageSerializer
            obj = GcsStorageSerializer()
            assert obj is not None

        def test_not_configured_raises(self):
            from enterprise.api.v2.gcs_storage import GcsStorageSerializer
            obj = GcsStorageSerializer()
            with pytest.raises(RuntimeError):
                obj.execute()

        def test_configure_and_validate(self):
            from enterprise.api.v2.gcs_storage import GcsStorageSerializer
            obj = GcsStorageSerializer()
            obj.configure(key="value")
            assert obj.validate() is True

        def test_repr(self):
            from enterprise.api.v2.gcs_storage import GcsStorageSerializer
            obj = GcsStorageSerializer()
            assert "GcsStorageSerializer" in repr(obj)
