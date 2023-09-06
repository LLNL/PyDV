import os
import numpy as np
import sys
from pydv import pdv

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


def test_read():
    main = pdv.Command()
    main.app = pdv.QApplication([])
    main.plotter = pdv.pdvplot.Plotter(main)
    main.do_readsina(os.path.join(TEST_DIR, 'testSinaData.json'))
    assert len(main.curvelist) == 2

    curve_1 = main.curvelist[0]
    curve_2 = main.curvelist[1]
    assert curve_1.name == 'darkness vs cycle (lux_cycle_series)'
    assert curve_2.name == 'lightness vs cycle (lux_cycle_series)'

    # darkness
    np.testing.assert_allclose(curve_1.y, np.array([0, 1, 4, 9, 16]))
    # lightness
    np.testing.assert_allclose(curve_2.y, np.array([5, 4, 2.5, 2.1, 2.0]))

    # do_xlabelwidth
    main.do_xlabelwidth('')
    assert main.xlabelwidth == 10

    main.do_xlabelwidth('15')
    assert main.xlabelwidth == 15

    # do_ylabelwidth
    main.do_ylabelwidth('')
    assert main.ylabelwidth == 10

    main.do_ylabelwidth('15')
    assert main.ylabelwidth == 15

    # do_filenamewidth
    main.do_filenamewidth('')
    assert main.filenamewidth == 30

    main.do_filenamewidth('35')
    assert main.filenamewidth == 35

    # do_recordidwidth
    main.do_recordidwidth('')
    assert main.recordidwidth == 10

    main.do_recordidwidth('15')
    assert main.recordidwidth == 15

    # read space-delimited txt
    main.do_read(os.path.join(TEST_DIR, 'testData.txt'))
    assert len(main.curvelist) == 4

    curve_3 = main.curvelist[2]
    curve_4 = main.curvelist[3]
    assert curve_3.name == 'darkness'
    assert curve_4.name == 'lightness'

    # darkness
    np.testing.assert_allclose(curve_3.y, np.array([0, 1, 4, 9, 16]))
    # lightness
    np.testing.assert_allclose(curve_4.y, np.array([5, 4, 2.5, 2.1, 2.0]))

    # read tab-delimited ult
    main.do_read(os.path.join(TEST_DIR, 'testData.ult'))
    assert len(main.curvelist) == 6

    curve_5 = main.curvelist[4]
    curve_6 = main.curvelist[5]
    assert curve_5.name == 'darkness'
    assert curve_6.name == 'lightness'

    # darkness
    np.testing.assert_allclose(curve_5.y, np.array([0, 1, 4, 9, 16]))
    # lightness
    np.testing.assert_allclose(curve_6.y, np.array([5, 4, 2.5, 2.1, 2.0]))

    # create and save gaussian curves
    main.do_gaussian('1 1 5')
    main.do_gaussian('1 1 1')
    main.do_save(os.path.join(TEST_DIR, 'testSave.txt') + ' a:b')

    # read saved gaussian curves
    main.do_read(os.path.join(TEST_DIR, 'testSave.txt'))
    assert len(main.curvelist) == 8

    curve_7 = main.curvelist[6]
    curve_8 = main.curvelist[7]
    assert curve_7.name == 'Gaussian'
    assert curve_8.name == 'Gaussian'
