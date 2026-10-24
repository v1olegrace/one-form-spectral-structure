"""Reproduction must reject nonfinite values and obey its stated binary64 budget."""
import importlib.util
import math
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location('num_compare', Path(__file__).resolve().parents[1]/'scripts/compare_numerical_outputs.py')
cmp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cmp)


@pytest.mark.parametrize('a,b', [(1., math.inf), (math.inf, math.inf),
                                 (-math.inf, math.inf), (math.nan, math.nan)])
def test_nonfinite_scientific_output_is_rejected(a, b):
    assert cmp.differences({'Gamma': a}, {'Gamma': b})


@pytest.mark.parametrize('x,direction', [(1.75, math.inf), (-1.75, -math.inf),
                                        (1., 0.), (0., math.inf), (-0., -math.inf)])
def test_eighth_step_accepted_ninth_step_rejected(x, direction):
    y = x
    for _ in range(8):
        y = math.nextafter(y, direction)
    assert cmp.differences({'x': x}, {'x': y}) == []
    y = math.nextafter(y, direction)
    assert cmp.differences({'x': x}, {'x': y})


def test_signed_zero_and_adjacent_subnormals():
    tiny = math.ulp(0.)
    assert cmp.differences(-0., 0.) == []
    assert cmp.differences(-4*tiny, 4*tiny) == []
    assert cmp.differences(-4*tiny, 5*tiny)
