"""Tests for enterprise.projects.image_resize."""
    import pytest
    class TestImageResizeClient:
        def test_init(self):
            from enterprise.projects.image_resize import ImageResizeClient
            obj = ImageResizeClient()
            assert obj is not None

        def test_not_configured_raises(self):
            from enterprise.projects.image_resize import ImageResizeClient
            obj = ImageResizeClient()
            with pytest.raises(RuntimeError):
                obj.execute()

        def test_configure_and_validate(self):
            from enterprise.projects.image_resize import ImageResizeClient
            obj = ImageResizeClient()
            obj.configure(key="value")
            assert obj.validate() is True

        def test_repr(self):
            from enterprise.projects.image_resize import ImageResizeClient
            obj = ImageResizeClient()
            assert "ImageResizeClient" in repr(obj)
