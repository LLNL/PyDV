
import os
import shutil
import subprocess

from matplotlib import image
from numpy import testing as np

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PYDV_DIR = os.path.dirname(TEST_DIR)
BASELINE_DIR = os.path.join(TEST_DIR, 'baseline')

# ------------------------ #
# --- Prepare the data --- #
# ------------------------ #

def test_execute():
    # The output directory will store the generated images to compare against the baseline
    output_dir = os.path.join(TEST_DIR, 'output')
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    # Generate a list of commands for PyDV to process. Between each command, we will
    # place an "image" statement, which will cause PyDV to save the current state of
    # the plot.
    commands = [
    f"""rd {os.path.join(TEST_DIR, "testData.txt")}
    cur 1 2""",
    "legend off",
    "erase",
    """cur 1 2
    L1 a b""",
    "L2 a b  3.0 5.5",
    "del c d",
    "color a blue",
    "color a red",
    "add a b",
    "annot FOO 3 7",
    "convolve a b",
    """del d
    copy a""",
    "cos a",
    """del d
    dashstyle b [2, 2, 4, 2]""",
    "dataid off",
    """dataid on
    delannot 1""",
    "derivative a",
    """del d
    dy b 2.5
    dx b 3""",
    """dx b -3
    divide c a""",
    """del d
    divx c 2
    divy c 2""",
    "dom 0 10",
    "dom de",
    "exp a",
    "log a",
    "grid off",
    """grid on
    integrate a""",
    """del d
    linespoints a on
    marker a . 20""",
    "lnwidth b 10",
    """lnwidth b 3
    makecurve (1 2 3) (5 2 3)""",
    """del d
    mx c 2""",
    "my a 3",
    "recip a",
    "scatter b on",
    """scatter b off
    cos b""",
    "acos b",
    "cosh b",
    "acosh b",
    "sin c",
    "asin c",
    "sinh c",
    "asinh c",
    "sqr b",
    "sqrt b",
    "sqrx b",
    "sqrtx b",
    "tan a",
    "atan a",
    "tanh a",
    "atanh a",
    "a - b",
    """del d
    b ** 2""",
    "c / b",
    "smooth d",
    """dy d -3
    abs d"""
    ]
    commands_file = os.path.join(output_dir, 'pydv_commands')
    with open(commands_file, 'w') as fp:
        for i, command in enumerate(commands):
            image_file = os.path.join(output_dir, f"test_image_{i+1:02d}")
            fp.write(command)
            fp.write(f"\nimage {image_file} png\n\n")
        fp.write("\nquit")

    # Execute PyDv
    exec_command = f"{os.path.join(PYDV_DIR, 'pydv', 'pdv')} -i {commands_file}"
    process = subprocess.Popen(exec_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


# ----------------- #
# --- Run tests --- #
# ----------------- #

# Helper text to generate the below tests for pytest
# with open('delete_me.txt', 'w') as fp:
#     for i in range(54):
#         filename = f"test_image_{i+1:02d}.png"
#         statement=f"""
# def test_image_{i+1:02d}():
#     baseline = image.imread(os.path.join(BASELINE_DIR, '{filename}'))
#     output = image.imread(os.path.join(output_dir, '{filename}'))
#     np.assert_equal(baseline, output)
# """
#         fp.write(statement)
#         statement = ''

# def test_image_01():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_01.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_01.png'))
#     np.assert_equal(baseline, output)

# def test_image_02():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_02.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_02.png'))
#     np.assert_equal(baseline, output)

# def test_image_03():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_03.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_03.png'))
#     np.assert_equal(baseline, output)

# def test_image_04():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_04.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_04.png'))
#     np.assert_equal(baseline, output)

# def test_image_05():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_05.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_05.png'))
#     np.assert_equal(baseline, output)

# def test_image_06():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_06.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_06.png'))
#     np.assert_equal(baseline, output)

# def test_image_07():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_07.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_07.png'))
#     np.assert_equal(baseline, output)

# def test_image_08():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_08.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_08.png'))
#     np.assert_equal(baseline, output)

# def test_image_09():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_09.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_09.png'))
#     np.assert_equal(baseline, output)

# def test_image_10():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_10.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_10.png'))
#     np.assert_equal(baseline, output)

# def test_image_11():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_11.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_11.png'))
#     np.assert_equal(baseline, output)

# def test_image_12():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_12.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_12.png'))
#     np.assert_equal(baseline, output)

# def test_image_13():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_13.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_13.png'))
#     np.assert_equal(baseline, output)

# def test_image_14():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_14.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_14.png'))
#     np.assert_equal(baseline, output)

# def test_image_15():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_15.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_15.png'))
#     np.assert_equal(baseline, output)

# def test_image_16():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_16.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_16.png'))
#     np.assert_equal(baseline, output)

# def test_image_17():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_17.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_17.png'))
#     np.assert_equal(baseline, output)

# def test_image_18():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_18.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_18.png'))
#     np.assert_equal(baseline, output)

# def test_image_19():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_19.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_19.png'))
#     np.assert_equal(baseline, output)

# def test_image_20():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_20.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_20.png'))
#     np.assert_equal(baseline, output)

# def test_image_21():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_21.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_21.png'))
#     np.assert_equal(baseline, output)

# def test_image_22():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_22.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_22.png'))
#     np.assert_equal(baseline, output)

# def test_image_23():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_23.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_23.png'))
#     np.assert_equal(baseline, output)

# def test_image_24():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_24.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_24.png'))
#     np.assert_equal(baseline, output)

# def test_image_25():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_25.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_25.png'))
#     np.assert_equal(baseline, output)

# def test_image_26():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_26.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_26.png'))
#     np.assert_equal(baseline, output)

# def test_image_27():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_27.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_27.png'))
#     np.assert_equal(baseline, output)

# def test_image_28():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_28.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_28.png'))
#     np.assert_equal(baseline, output)

# def test_image_29():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_29.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_29.png'))
#     np.assert_equal(baseline, output)

# def test_image_30():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_30.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_30.png'))
#     np.assert_equal(baseline, output)

# def test_image_31():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_31.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_31.png'))
#     np.assert_equal(baseline, output)

# def test_image_32():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_32.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_32.png'))
#     np.assert_equal(baseline, output)

# def test_image_33():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_33.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_33.png'))
#     np.assert_equal(baseline, output)

# def test_image_34():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_34.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_34.png'))
#     np.assert_equal(baseline, output)

# def test_image_35():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_35.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_35.png'))
#     np.assert_equal(baseline, output)

# def test_image_36():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_36.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_36.png'))
#     np.assert_equal(baseline, output)

# def test_image_37():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_37.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_37.png'))
#     np.assert_equal(baseline, output)

# def test_image_38():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_38.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_38.png'))
#     np.assert_equal(baseline, output)

# def test_image_39():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_39.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_39.png'))
#     np.assert_equal(baseline, output)

# def test_image_40():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_40.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_40.png'))
#     np.assert_equal(baseline, output)

# def test_image_41():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_41.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_41.png'))
#     np.assert_equal(baseline, output)

# def test_image_42():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_42.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_42.png'))
#     np.assert_equal(baseline, output)

# def test_image_43():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_43.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_43.png'))
#     np.assert_equal(baseline, output)

# def test_image_44():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_44.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_44.png'))
#     np.assert_equal(baseline, output)

# def test_image_45():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_45.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_45.png'))
#     np.assert_equal(baseline, output)

# def test_image_46():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_46.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_46.png'))
#     np.assert_equal(baseline, output)

# def test_image_47():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_47.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_47.png'))
#     np.assert_equal(baseline, output)

# def test_image_48():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_48.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_48.png'))
#     np.assert_equal(baseline, output)

# def test_image_49():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_49.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_49.png'))
#     np.assert_equal(baseline, output)

# def test_image_50():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_50.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_50.png'))
#     np.assert_equal(baseline, output)

# def test_image_51():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_51.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_51.png'))
#     np.assert_equal(baseline, output)

# def test_image_52():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_52.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_52.png'))
#     np.assert_equal(baseline, output)

# def test_image_53():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_53.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_53.png'))
#     np.assert_equal(baseline, output)

# def test_image_54():
#     baseline = image.imread(os.path.join(BASELINE_DIR, 'test_image_54.png'))
#     output = image.imread(os.path.join(output_dir, 'test_image_54.png'))
#     np.assert_equal(baseline, output)
