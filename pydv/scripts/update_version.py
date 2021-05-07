
import os
import argparse
import fileinput

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print(ROOT_DIR)

# Get the version number from the version file
version_file = os.path.join(SCRIPTS_DIR, 'version.txt')
with open(version_file, 'r') as fp:
    version = fp.read()
    version_list = version.split('.')
    major, minor, patch = int(version_list[0]), int(version_list[1]), int(version_list[2])

# Determine the new version from the specified type of change
parser = argparse.ArgumentParser()
parser.add_argument('type', choices=['major', 'minor', 'patch'])
args = parser.parse_args().type
if args == 'major':
    major += 1
    minor = 0
    patch = 0
elif args == 'minor':
    minor += 1
    patch = 0
elif args == 'patch':
    patch += 1
new_version = f'{major}.{minor}.{patch}'

# Replace the version everwhere in the source code where it appears.
files = [
    os.path.join(ROOT_DIR, 'setup.py'),
    os.path.join(SOURCE_DIR, 'pdvplot.py'),
    os.path.join(SOURCE_DIR, 'pdv.py'),
    os.path.join(SOURCE_DIR, 'docs', 'conf.py'),
    os.path.join(SCRIPTS_DIR, 'version.txt'),
]
for file in files:
    with fileinput.FileInput(file, inplace=True) as file:
        for line in file:
            print(line.replace(version, new_version), end='')

# Special case: the conf.py file also wants a representation of just major.minor
with fileinput.FileInput(os.path.join(SOURCE_DIR, 'docs', 'conf.py'), inplace=True) as file:
    for line in file:
        
        print(line.replace(f'{version_list[0]}.{version_list[1]}', f'{major}.{minor}'), end='')

# TODO: Add section on Release notes for PyDV new_version to the release notes
# file

print(new_version)
x = []

