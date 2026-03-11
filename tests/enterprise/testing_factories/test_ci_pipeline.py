"""Tests for enterprise.testing.factories.ci_pipeline."""
    import pytest
    class TestCiPipelineFactory:
        def test_init(self):
            from enterprise.testing.factories.ci_pipeline import CiPipelineFactory
            obj = CiPipelineFactory()
            assert obj is not None

        def test_not_configured_raises(self):
            from enterprise.testing.factories.ci_pipeline import CiPipelineFactory
            obj = CiPipelineFactory()
            with pytest.raises(RuntimeError):
                obj.execute()

        def test_configure_and_validate(self):
            from enterprise.testing.factories.ci_pipeline import CiPipelineFactory
            obj = CiPipelineFactory()
            obj.configure(key="value")
            assert obj.validate() is True

        def test_repr(self):
            from enterprise.testing.factories.ci_pipeline import CiPipelineFactory
            obj = CiPipelineFactory()
            assert "CiPipelineFactory" in repr(obj)
