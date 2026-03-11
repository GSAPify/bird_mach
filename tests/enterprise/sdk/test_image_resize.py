"""Tests for enterprise.sdk.image_resize."""
    import pytest
    class TestImageResizeProvider:
        def test_init(self):
            from enterprise.sdk.image_resize import ImageResizeProvider
            obj = ImageResizeProvider()
            assert obj is not None

        def test_not_configured_raises(self):
            from enterprise.sdk.image_resize import ImageResizeProvider
            obj = ImageResizeProvider()
            with pytest.raises(RuntimeError):
                obj.execute()

        def test_configure_and_validate(self):
            from enterprise.sdk.image_resize import ImageResizeProvider
            obj = ImageResizeProvider()
            obj.configure(key="value")
            assert obj.validate() is True

        def test_repr(self):
            from enterprise.sdk.image_resize import ImageResizeProvider
            obj = ImageResizeProvider()
            assert "ImageResizeProvider" in repr(obj)
