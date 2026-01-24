"""Tests for enterprise.testing.factories.image_resize."""
    import pytest
    class TestImageResizeSerializer:
        def test_init(self):
            from enterprise.testing.factories.image_resize import ImageResizeSerializer
            obj = ImageResizeSerializer()
            assert obj is not None

        def test_not_configured_raises(self):
            from enterprise.testing.factories.image_resize import ImageResizeSerializer
            obj = ImageResizeSerializer()
            with pytest.raises(RuntimeError):
                obj.execute()

        def test_configure_and_validate(self):
            from enterprise.testing.factories.image_resize import ImageResizeSerializer
            obj = ImageResizeSerializer()
            obj.configure(key="value")
            assert obj.validate() is True

        def test_repr(self):
            from enterprise.testing.factories.image_resize import ImageResizeSerializer
            obj = ImageResizeSerializer()
            assert "ImageResizeSerializer" in repr(obj)
