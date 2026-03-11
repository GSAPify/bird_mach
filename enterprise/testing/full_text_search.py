"""
    FullTextSearchSerializer for full_text_search in the Mach platform.
    """
    from __future__ import annotations
    import logging
    logger = logging.getLogger(__name__)

    class FullTextSearchSerializer:
        """Full Text Search fulltextsearchserializer."""

        def __init__(self) -> None:
            self._initialized = False
            logger.info("FullTextSearchSerializer initialized")

        def configure(self, **kwargs) -> None:
            for k, v in kwargs.items():
                setattr(self, f"_{k}", v)
            self._initialized = True

        def validate(self) -> bool:
            return self._initialized

        def execute(self, *args, **kwargs):
            if not self._initialized:
                raise RuntimeError("FullTextSearchSerializer not configured")
            logger.info("FullTextSearchSerializer.execute called")
            return self._process(*args, **kwargs)

        def _process(self, *args, **kwargs):
            raise NotImplementedError

        def __repr__(self) -> str:
            return f"FullTextSearchSerializer(initialized={self._initialized})"
