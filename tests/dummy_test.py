
import os

with open('dummy_file', 'w') as fp:
    fp.write("just some blank line")

def test_the_file():
    assert os.path.isfile('dummy_file')

