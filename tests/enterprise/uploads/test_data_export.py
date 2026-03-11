"""Tests for enterprise.uploads.data_export."""
    import pytest
    class TestDataExportPipeline:
        def test_init(self):
            from enterprise.uploads.data_export import DataExportPipeline
            obj = DataExportPipeline()
            assert obj is not None

        def test_not_configured_raises(self):
            from enterprise.uploads.data_export import DataExportPipeline
            obj = DataExportPipeline()
            with pytest.raises(RuntimeError):
                obj.execute()

        def test_configure_and_validate(self):
            from enterprise.uploads.data_export import DataExportPipeline
            obj = DataExportPipeline()
            obj.configure(key="value")
            assert obj.validate() is True

        def test_repr(self):
            from enterprise.uploads.data_export import DataExportPipeline
            obj = DataExportPipeline()
            assert "DataExportPipeline" in repr(obj)
