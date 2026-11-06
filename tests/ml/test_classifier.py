"""Tests for audio classifier."""
import numpy as np
from bird_mach.ml.classifier import AudioClassifier

class TestAudioClassifier:
    def test_fit_predict(self):
        clf = AudioClassifier(k=3)
        features = [np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1]),
                    np.array([1.1, 0, 0]), np.array([0, 1.1, 0])]
        labels = ["rock", "jazz", "classical", "rock", "jazz"]
        clf.fit(features, labels)
        pred = clf.predict(np.array([1, 0.1, 0]))
        assert pred.label == "rock"
        assert pred.confidence > 0.5

    def test_empty(self):
        clf = AudioClassifier()
        pred = clf.predict(np.array([1, 2, 3]))
        assert pred.label == "unknown"


def test_fit_is_isolated_from_caller_mutation():
    import numpy as np
    from bird_mach.ml.classifier import AudioClassifier
    feats, labels = [np.array([0.0, 0.0])], ["a"]
    clf = AudioClassifier(k=1)
    clf.fit(feats, labels)
    labels[0] = "b"
    feats[0][:] = 100
    assert clf.predict(np.array([0.0, 0.0])).label == "a"
