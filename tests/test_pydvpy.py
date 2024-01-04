import os
import pathlib
import pytest
import numpy as np
import sys


TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PYDV_DIR = os.path.dirname(TEST_DIR)

sys.path.append(os.path.join(PYDV_DIR, "pydv"))
import pydvpy  # noqa E402


test_files = list(pathlib.Path(TEST_DIR).glob('testData.*'))


@pytest.mark.parametrize("test_file", test_files)
def test_read(test_file):
    curves = pydvpy.read(test_file)

    # darkness
    np.testing.assert_array_equal(curves[0].y, [0, 1, 4, 9, 16])

    # lightness
    np.testing.assert_array_equal(curves[1].y, [5, 4, 2.5, 2.1, 2.0])


def test_sinaread():
    curves = pydvpy.readsina(os.path.join(TEST_DIR, 'testSinaData.json'))

    # darkness curve
    np.testing.assert_array_equal(curves[0].y, [0, 1, 4, 9, 16])

    # darkness curve record id
    assert curves[0].record_id == "sinaTest_1"

    # lightness
    np.testing.assert_array_equal(curves[1].y, [5, 4, 2.5, 2.1, 2.0])

    # lightness curve record id
    assert curves[1].record_id == "sinaTest_1"


test_files = list(pathlib.Path(TEST_DIR).glob('testDataregex.*'))


@pytest.mark.parametrize("test_file", test_files)
def test_read_regex(test_file):

    # darkness
    curves = pydvpy.read(test_file, pattern='darkness')
    np.testing.assert_array_equal(curves[0].y, [0, 1, 4, 9, 16])
    np.testing.assert_array_equal(curves[1].y, [0, 1, 4, 9, 16])
    np.testing.assert_array_equal(curves[2].y, [0, 1, 4, 9, 16])

    # lightness
    curves = pydvpy.read(test_file, pattern='lightness')
    np.testing.assert_array_equal(curves[0].y, [5, 4, 2.5, 2.1, 2.0])
    np.testing.assert_array_equal(curves[1].y, [5, 4, 2.5, 2.1, 2.0])
    np.testing.assert_array_equal(curves[2].y, [5, 4, 2.5, 2.1, 2.0])

    # 2
    curves = pydvpy.read(test_file, pattern='2')
    np.testing.assert_array_equal(curves[0].y, [0, 1, 4, 9, 16])
    np.testing.assert_array_equal(curves[1].y, [5, 4, 2.5, 2.1, 2.0])

    # 3
    curves = pydvpy.read(test_file, pattern='3')
    np.testing.assert_array_equal(curves[0].y, [0, 1, 4, 9, 16])
    np.testing.assert_array_equal(curves[1].y, [5, 4, 2.5, 2.1, 2.0])


def test_read_labels():

    test_file = os.path.join(TEST_DIR, 'labels.txt')
    curves = pydvpy.read(test_file)
    xlabels = ['0Time',
               '',
               '1aTime [seconds]',
               '1bTime [seconds]',
               '',
               '',
               '3aTime [seconds]',
               '3bTime [seconds]',
               '4aTime [seconds]',
               '4bTime [seconds]',
               '5aTime [seconds]',
               '5bTime [seconds]',
               '',
               '',
               '7aTime [seconds]',
               '7bTime [seconds]',
               '8aTime [seconds]',
               '8bTime [seconds]',
               '',
               '10aTime [seconds]']
    ylabels = ['',
               '',
               '',
               '',
               '2aTemperature [K]',
               '2bTemperature [K]',
               '3aTemperature [K]',
               '3bTemperature [K]',
               '4aTemperature [K]',
               '4bTemperature [K]',
               '',
               '',
               '6aTemperature [K]',
               '6bTemperature [K]',
               '7aTemperature [K]',
               '7bTemperature [K]',
               '8aTemperature [K]',
               '8bTemperature [K]',
               '',
               ''
               ]

    for i, cur in enumerate(curves):
        assert cur.xlabel == xlabels[i]
        assert cur.ylabel == ylabels[i]

    test_file = os.path.join(TEST_DIR, 'labels2.txt')

    pydvpy.save(test_file, curves, verbose=False, save_labels=True)

    curves = pydvpy.read(test_file)

    for i, cur in enumerate(curves):
        assert cur.xlabel == xlabels[i]
        assert cur.ylabel == ylabels[i]
