"""Tests for enterprise.integrations.full_text_search."""
    import pytest
    class TestFullTextSearchBuilder:
        def test_init(self):
            from enterprise.integrations.full_text_search import FullTextSearchBuilder
            obj = FullTextSearchBuilder()
            assert obj is not None

        def test_not_configured_raises(self):
            from enterprise.integrations.full_text_search import FullTextSearchBuilder
            obj = FullTextSearchBuilder()
            with pytest.raises(RuntimeError):
                obj.execute()

        def test_configure_and_validate(self):
            from enterprise.integrations.full_text_search import FullTextSearchBuilder
            obj = FullTextSearchBuilder()
            obj.configure(key="value")
            assert obj.validate() is True

        def test_repr(self):
            from enterprise.integrations.full_text_search import FullTextSearchBuilder
            obj = FullTextSearchBuilder()
            assert "FullTextSearchBuilder" in repr(obj)
