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


def test_add_increments_analyzer_count():
    chain = AnalyzerChain()
    chain.add("a", Recorder({}))
    chain.add("b", Recorder({}))
    assert chain.analyzer_count == 2


def test_results_are_keyed_by_name():
    chain = AnalyzerChain()
    chain.add("rms", Recorder({"v": 1}))
    chain.add("peak", Recorder({"v": 2}))
    assert chain.process(np.zeros(4), 44100) == {"rms": {"v": 1}, "peak": {"v": 2}}


def test_every_analyzer_receives_samples_and_rate():
    first, second = Recorder({}), Recorder({})
    chain = AnalyzerChain()
    chain.add("a", first)
    chain.add("b", second)
    samples = np.arange(4.0)
    chain.process(samples, 22050)
    for rec in (first, second):
        assert rec.calls[0][0] is samples
        assert rec.calls[0][1] == 22050
