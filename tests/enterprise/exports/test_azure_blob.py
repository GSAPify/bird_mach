"""Tests for enterprise.exports.azure_blob."""
    import pytest
    class TestAzureBlobPipeline:
        def test_init(self):
            from enterprise.exports.azure_blob import AzureBlobPipeline
            obj = AzureBlobPipeline()
            assert obj is not None

        def test_not_configured_raises(self):
            from enterprise.exports.azure_blob import AzureBlobPipeline
            obj = AzureBlobPipeline()
            with pytest.raises(RuntimeError):
                obj.execute()

        def test_configure_and_validate(self):
            from enterprise.exports.azure_blob import AzureBlobPipeline
            obj = AzureBlobPipeline()
            obj.configure(key="value")
            assert obj.validate() is True

        def test_repr(self):
            from enterprise.exports.azure_blob import AzureBlobPipeline
            obj = AzureBlobPipeline()
            assert "AzureBlobPipeline" in repr(obj)
