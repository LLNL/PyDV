import os
import shutil
import subprocess
import pytest

from matplotlib import image
import numpy as np


TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PYDV_DIR = os.path.dirname(TEST_DIR)
BASELINE_DIR = os.path.join(TEST_DIR, 'baseline')

# ------------------------ #
# --- Prepare the data --- #
# ------------------------ #

# The output directory will store the generated images to compare against the baseline
output_dir = os.path.join(TEST_DIR, 'output')
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir)

# Generate a list of commands for PyDV to process. Between each command, we will
# place an "image" statement, which will cause PyDV to save the current state of
# the plot.
commands = [
f"""rd {os.path.join(TEST_DIR, 'testData.txt')}
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
abs d""",
"""erase
legend on
gaussian 1 1 5""",
"exp A",
"log A",
"expx A",
"logx A",
"""exp A
sin A
log A""",
f"""readsina {os.path.join(TEST_DIR, 'testSinaData.json')}
readsina {os.path.join(TEST_DIR, 'testSinaData2.json')}
cur 3 4 5 6
labelcurve on""",
"""labelcurve off
labelrecordids on""",
f"""labelrecordids off
read {os.path.join(TEST_DIR, 'testData.ult')}
cur 7 8
group""",
"""labelfilenames on""",
"""labelfilenames off"""
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

test_images = [_ for _ in os.listdir(output_dir) if _.endswith(".png")]
baseline_images = [_ for _ in os.listdir(BASELINE_DIR) if _.endswith(".png")]

@pytest.mark.parametrize("baseline_image, test_image",  list(zip(baseline_images, test_images)))
def test_image(baseline_image, test_image):
    baseline = image.imread(os.path.join(BASELINE_DIR, baseline_image))
    output = image.imread(os.path.join(output_dir, test_image))
    np.array_equal(baseline, output)

# ----------------- #
# --- Run tests --- #
# ----------------- #

# # Helper text to generate the below tests for pytest
# with open('delete_me.txt', 'w') as fp:
#     for i in range(60):
#         filename = f"test_image_{i+1:02d}.png"
#         statement=f"""
# def test_image_{i+1:02d}():
#     baseline = image.imread(os.path.join(BASELINE_DIR, '{filename}'))
#     output = image.imread(os.path.join(output_dir, '{filename}'))
#     np.assert_equal(baseline, output)
# """
#         fp.write(statement)
#         statement = ''
