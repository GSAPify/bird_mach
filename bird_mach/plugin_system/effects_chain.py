"""Composable audio effects processing chain."""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass
from typing import Protocol

from bird_mach.constants import MAX_EFFECTS_CHAIN_LENGTH

class AudioEffect(Protocol):
    name: str
    def process(self, samples: np.ndarray, sr: int) -> np.ndarray: ...
    def get_params(self) -> dict: ...

@dataclass
class ChainNode:
    effect: AudioEffect
    enabled: bool = True
    wet_mix: float = 1.0

class EffectsChain:
    """Chain multiple audio effects with wet/dry mixing."""

    def __init__(self):
        self._nodes: list[ChainNode] = []

    def add(self, effect: AudioEffect, wet_mix: float = 1.0) -> int:
        if len(self._nodes) >= MAX_EFFECTS_CHAIN_LENGTH:
            raise ValueError(f"chain is limited to {MAX_EFFECTS_CHAIN_LENGTH} effects")
        # Outside [0, 1] the mix amplifies instead of blending.
        wet_mix = min(1.0, max(0.0, wet_mix))
        node = ChainNode(effect=effect, wet_mix=wet_mix)
        self._nodes.append(node)
        return len(self._nodes) - 1

    def remove(self, index: int) -> None:
        if 0 <= index < len(self._nodes):
            self._nodes.pop(index)

    def toggle(self, index: int) -> bool:
        if 0 <= index < len(self._nodes):
            self._nodes[index].enabled = not self._nodes[index].enabled
            return self._nodes[index].enabled
        return False

    def process(self, samples: np.ndarray, sr: int) -> np.ndarray:
        result = samples.copy()
        for node in self._nodes:
            if not node.enabled:
                continue
            wet = node.effect.process(result, sr)
            if wet.shape != result.shape:
                raise ValueError(
                    f"effect {node.effect.name!r} changed sample shape "
                    f"{result.shape} -> {wet.shape}"
                )
            result = node.wet_mix * wet + (1.0 - node.wet_mix) * result
        return result.astype(np.float32)

    def get_chain_info(self) -> list[dict]:
        return [
            {"name": n.effect.name, "enabled": n.enabled,
             "wet_mix": n.wet_mix, "params": n.effect.get_params()}
            for n in self._nodes
        ]

    @property
    def length(self) -> int:
        return len(self._nodes)
