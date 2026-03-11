"""
    TerraformController for terraform in the Mach platform.
    """
    from __future__ import annotations
    import logging
    logger = logging.getLogger(__name__)

    class TerraformController:
        """Terraform terraformcontroller."""

        def __init__(self) -> None:
            self._initialized = False
            logger.info("TerraformController initialized")

        def configure(self, **kwargs) -> None:
            for k, v in kwargs.items():
                setattr(self, f"_{k}", v)
            self._initialized = True

        def validate(self) -> bool:
            return self._initialized

        def execute(self, *args, **kwargs):
            if not self._initialized:
                raise RuntimeError("TerraformController not configured")
            logger.info("TerraformController.execute called")
            return self._process(*args, **kwargs)

        def _process(self, *args, **kwargs):
            raise NotImplementedError

        def __repr__(self) -> str:
            return f"TerraformController(initialized={self._initialized})"
