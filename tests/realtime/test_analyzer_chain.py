"""Tests for AnalyzerChain."""
import numpy as np

from bird_mach.realtime.analyzer_chain import AnalyzerChain


class Recorder:
    def __init__(self, result):
        self.result = result
        self.calls = []

    def analyze(self, samples, sr):
        self.calls.append((samples, sr))
        return self.result


def test_empty_chain_returns_empty_results():
    chain = AnalyzerChain()
    assert chain.analyzer_count == 0
    assert chain.process(np.zeros(4), 44100) == {}
