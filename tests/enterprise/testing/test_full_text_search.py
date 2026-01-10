"""Tests for enterprise.testing.full_text_search."""
    import pytest
    class TestFullTextSearchSerializer:
        def test_init(self):
            from enterprise.testing.full_text_search import FullTextSearchSerializer
            obj = FullTextSearchSerializer()
            assert obj is not None

        def test_not_configured_raises(self):
            from enterprise.testing.full_text_search import FullTextSearchSerializer
            obj = FullTextSearchSerializer()
            with pytest.raises(RuntimeError):
                obj.execute()

        def test_configure_and_validate(self):
            from enterprise.testing.full_text_search import FullTextSearchSerializer
            obj = FullTextSearchSerializer()
            obj.configure(key="value")
            assert obj.validate() is True

        def test_repr(self):
            from enterprise.testing.full_text_search import FullTextSearchSerializer
            obj = FullTextSearchSerializer()
            assert "FullTextSearchSerializer" in repr(obj)
