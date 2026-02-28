"""Type aliases used across the Mach codebase."""

from __future__ import annotations

from typing import TypeAlias

import numpy as np
import numpy.typing as npt

AudioArray: TypeAlias = npt.NDArray[np.float32]
FeatureMatrix: TypeAlias = npt.NDArray[np.float32]
EmbeddingMatrix: TypeAlias = npt.NDArray[np.float32]
TimeArray: TypeAlias = npt.NDArray[np.float32]
EnergyArray: TypeAlias = npt.NDArray[np.float32]
