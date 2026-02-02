"""Tests for enterprise.cache.image_resize."""
    import pytest
    class TestImageResizeFactory:
        def test_init(self):
            from enterprise.cache.image_resize import ImageResizeFactory
            obj = ImageResizeFactory()
            assert obj is not None

        def test_not_configured_raises(self):
            from enterprise.cache.image_resize import ImageResizeFactory
            obj = ImageResizeFactory()
            with pytest.raises(RuntimeError):
                obj.execute()

        def test_configure_and_validate(self):
            from enterprise.cache.image_resize import ImageResizeFactory
            obj = ImageResizeFactory()
            obj.configure(key="value")
            assert obj.validate() is True

        def test_repr(self):
            from enterprise.cache.image_resize import ImageResizeFactory
            obj = ImageResizeFactory()
            assert "ImageResizeFactory" in repr(obj)
