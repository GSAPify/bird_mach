"""Tests for data augmentation."""
import numpy as np
from bird_mach.ml.data_augmentation import add_noise, time_shift, change_volume, time_mask

class TestAugmentation:
    def test_add_noise(self):
        y = np.zeros(1000, dtype=np.float32)
        noisy = add_noise(y, snr_db=10)
        assert not np.allclose(noisy, y)

    def test_time_shift(self):
        y = np.arange(100, dtype=np.float32)
        shifted = time_shift(y, shift_max=10)
        assert len(shifted) == len(y)

    def test_volume(self):
        y = np.ones(100, dtype=np.float32) * 0.5
        changed = change_volume(y, gain_db_range=(6, 6))
        assert np.max(changed) > np.max(y)

    def test_mask(self):
        y = np.ones(1000, dtype=np.float32)
        masked = time_mask(y, max_mask=100)
        assert np.any(masked == 0)
