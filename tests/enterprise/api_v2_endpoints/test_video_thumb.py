"""Tests for enterprise.api.v2.endpoints.video_thumb."""
    import pytest
    class TestVideoThumbClient:
        def test_init(self):
            from enterprise.api.v2.endpoints.video_thumb import VideoThumbClient
            obj = VideoThumbClient()
            assert obj is not None

        def test_not_configured_raises(self):
            from enterprise.api.v2.endpoints.video_thumb import VideoThumbClient
            obj = VideoThumbClient()
            with pytest.raises(RuntimeError):
                obj.execute()

        def test_configure_and_validate(self):
            from enterprise.api.v2.endpoints.video_thumb import VideoThumbClient
            obj = VideoThumbClient()
            obj.configure(key="value")
            assert obj.validate() is True

        def test_repr(self):
            from enterprise.api.v2.endpoints.video_thumb import VideoThumbClient
            obj = VideoThumbClient()
            assert "VideoThumbClient" in repr(obj)
