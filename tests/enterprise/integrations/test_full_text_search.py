"""Tests for enterprise.integrations.full_text_search."""
    import pytest
    class TestFullTextSearchRepository:
        def test_init(self):
            from enterprise.integrations.full_text_search import FullTextSearchRepository
            obj = FullTextSearchRepository()
            assert obj is not None

        def test_not_configured_raises(self):
            from enterprise.integrations.full_text_search import FullTextSearchRepository
            obj = FullTextSearchRepository()
            with pytest.raises(RuntimeError):
                obj.execute()

        def test_configure_and_validate(self):
            from enterprise.integrations.full_text_search import FullTextSearchRepository
            obj = FullTextSearchRepository()
            obj.configure(key="value")
            assert obj.validate() is True

        def test_repr(self):
            from enterprise.integrations.full_text_search import FullTextSearchRepository
            obj = FullTextSearchRepository()
            assert "FullTextSearchRepository" in repr(obj)
