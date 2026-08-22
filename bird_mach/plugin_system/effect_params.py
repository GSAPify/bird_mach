"""Parameterized effect configuration with validation."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class ParamSpec:
    name: str
    min_val: float
    max_val: float
    default: float
    unit: str = ""

    def __post_init__(self) -> None:
        if self.min_val > self.max_val:
            raise ValueError("min_val must not exceed max_val")
        if not self.min_val <= self.default <= self.max_val:
            raise ValueError("default must be within [min_val, max_val]")

    def validate(self, value: float) -> float:
        return max(self.min_val, min(self.max_val, value))

GAIN_PARAM = ParamSpec("gain", -60.0, 24.0, 0.0, "dB")
CUTOFF_PARAM = ParamSpec("cutoff", 20.0, 20000.0, 5000.0, "Hz")
RATIO_PARAM = ParamSpec("ratio", 1.0, 20.0, 4.0, ":1")
DECAY_PARAM = ParamSpec("decay", 0.0, 1.0, 0.3, "")
DELAY_PARAM = ParamSpec("delay", 1.0, 500.0, 40.0, "ms")
