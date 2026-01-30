"""Tests for enterprise.permissions.full_text_search."""
    import pytest
    class TestFullTextSearchValidator:
        def test_init(self):
            from enterprise.permissions.full_text_search import FullTextSearchValidator
            obj = FullTextSearchValidator()
            assert obj is not None

        def test_not_configured_raises(self):
            from enterprise.permissions.full_text_search import FullTextSearchValidator
            obj = FullTextSearchValidator()
            with pytest.raises(RuntimeError):
                obj.execute()

        def test_configure_and_validate(self):
            from enterprise.permissions.full_text_search import FullTextSearchValidator
            obj = FullTextSearchValidator()
            obj.configure(key="value")
            assert obj.validate() is True

        def test_repr(self):
            from enterprise.permissions.full_text_search import FullTextSearchValidator
            obj = FullTextSearchValidator()
            assert "FullTextSearchValidator" in repr(obj)
