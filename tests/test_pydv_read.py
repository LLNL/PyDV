import os
import pathlib
import pytest
import numpy as np
import sys
sys.path.append("./pydv")
import pydv.pydvpy as pydvpy

TEST_DIR = os.path.dirname(os.path.abspath(__file__))

test_files = list(pathlib.Path(TEST_DIR).glob('testData.*'))

@pytest.mark.parametrize("test_file",  test_files)
def test_read(test_file):
    curves = pydvpy.read(test_file)
    # darkness
    np.testing.assert_array_equal(curves[0].y, [0, 1, 4, 9, 16])
    # lightness
    np.testing.assert_array_equal(curves[1].y, [5, 4, 2.5, 2.1, 2.0])
