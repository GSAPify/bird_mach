"""Tests for ParamSpec validation."""
import math

from bird_mach.plugin_system.effect_params import CUTOFF_PARAM, GAIN_PARAM


def test_nan_and_inf_fall_back_to_default():
    assert GAIN_PARAM.validate(math.nan) == GAIN_PARAM.default
    assert CUTOFF_PARAM.validate(math.inf) == CUTOFF_PARAM.default


def test_finite_values_are_clamped():
    assert GAIN_PARAM.validate(100.0) == 24.0
    assert GAIN_PARAM.validate(-100.0) == -60.0
