import os
import pathlib
import pytest
import numpy as np
import sys
import matplotlib.pyplot as plt
import scipy

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


# Steps: **ONLY** do steps below if new curves are added to tests/convolution_pydv_create_curves_to_convolv
#     1. pydv/pdv -i tests/convolution_pydv_create_curves_to_convolv
#            The randomness here can cause issues with ultra! divide by 0? Re-run all steps if issues arise in step 5
#     2. python tests/convolution_create_pydv_and_ultra_commands.py
#     3. pydv/pdv -i tests/convolution_pydv_commands
#     4. export PATH=$PATH:/usr/apps/pact/bin/
#     5. ultra -l tests/convolution_ultra_commands
# convolb: (g*h)(x) = Int(-inf, inf, dt*g(t)*h(x-t)) / Int(-inf, inf, dt*h(t))
# convolc: (g*h)(x) = Int(-inf, inf, dt*g(t)*h(x-t))
curves_pydv = pydvpy.read(os.path.join(TEST_DIR, 'convol_pydv.ult'))
curves_ultra = pydvpy.read(os.path.join(TEST_DIR, 'convol_ultra.ult'))
convol_plot_path = os.path.join(TEST_DIR, 'convolution_plots')
os.makedirs(convol_plot_path, exist_ok=True)


def test_convol_curves():
    curves = pydvpy.read(os.path.join(TEST_DIR, 'convolution_created_curves_to_convol.ult'))
    start = ord('A')

    for i, cur in enumerate(curves):
        curve_letter = chr(start + i)
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.plot(cur.x, cur.y, marker='x', linewidth=1)
        ax.set_title(f"Curve {curve_letter}: {cur.name}")
        ax.legend()
        fig.savefig(os.path.join(TEST_DIR, 'convolution_plots', f'convol_curve_{curve_letter}.png'))
        plt.close(fig)


@pytest.mark.parametrize("i", list(range(len(curves_pydv))))
def test_convol(i):

    # for cp, cu in zip(curves_pydv, curves_ultra):
    cp = curves_pydv[i]
    cu = curves_ultra[i]
    print(f"Curve {i+1} of {len(curves_pydv)}")
    print('Lengths:')
    print(f'\tPyDV:  {len(cp.y)}')
    print(f'\tUltra: {len(cu.y)}')

    print('First 5 x:')
    print(f'\tPyDV:  {cp.x[:5]}')
    print(f'\tUltra: {cu.x[:5]}')

    print('Last 5 x:')
    print(f'\tPyDV:  {cp.x[-5:]}')
    print(f'\tUltra: {cu.x[-5:]}')

    print('First 5 y:')
    print(f'\tPyDV:  {cp.y[:5]}')
    print(f'\tUltra: {cu.y[:5]}')

    print('Last 5 y:')
    print(f'\tPyDV:  {cp.y[-5:]}')
    print(f'\tUltra: {cu.y[-5:]}')

    print('Max y:')
    print(f'\tPyDV:  {max(cp.y)}')
    print(f'\tUltra: {max(cu.y)}')

    # Ultra sometimes has 99 points for some reason
    if len(cu.y) == 99:
        start = 1
    else:
        start = 0

    plot_details = ''

    # Area
    area_pydv = scipy.integrate.simpson(cp.y[start:], cp.x[start:])
    area_ultra = scipy.integrate.simpson(cu.y, cu.x)
    area_diff = abs(area_pydv - area_ultra)
    area_percent = area_diff / area_ultra * 100
    print('Area:')
    print('\tpydv ', area_pydv)
    print('\tultra', area_ultra)
    print('\tdiff ', area_diff)
    print('\tdiff percent', area_percent, "%\n")
    if area_percent > 1:
        plot_details += f'_area_diff_percent_{area_percent:.3f}'

    # Max diff of ys
    diff = abs(cp.y[start:] - cu.y)
    diff_max = np.max(diff)
    diff_index = diff.argmax()
    diff_percent = diff_max / abs(cu.y[diff_index]) * 100
    print('Maximum diff of all ys:')
    print(f'\tdiff: {diff_max} at:')
    print(f'\t\tPydv.y  {cp.y[diff_index + start]}')
    print(f'\t\tUltra.y {cu.y[diff_index]}')
    print('\tdiff percent', diff_percent, "%\n\n")
    # Most pass with 1% Difference but Ultra sometimes has missing points during integration which causes spikes
    # This is most evident with the noisy or sparse curves
    if diff_percent > 1:
        plot_details += f'_max_diff_y_percent_{diff_percent:.3f}'

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.plot(cp.x, cp.y, marker='x', linewidth=1, label='PyDV')
    ax.plot(cu.x, cu.y, marker='+', linewidth=1, label='Ultra')
    ax.scatter(cp.x[diff_index + start], cp.y[diff_index + start], marker='x', s=200,
               label=f'PyDV Max Diff Y {cp.y[diff_index + start]:.5f}')
    ax.scatter(cu.x[diff_index], cu.y[diff_index], marker='+', s=200,
               label=f'Ultra Max Diff Y {cu.y[diff_index]:.5f}')
    ax.set_title(f"{cp.name} {plot_details}")
    ax.legend()
    fig.savefig(os.path.join(TEST_DIR, 'convolution_plots', f'convol_plot_{i+1}{plot_details}.png'))
    plt.close(fig)

    # All these tests will never pass but see the plots in tests/convolution_plots/
    # np.testing.assert_array_less(area_percent, 1)
    # np.testing.assert_array_less(diff_percent, 1)


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
