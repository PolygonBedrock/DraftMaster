from cx_Freeze import setup, Executable
import os
import sys
import shutil
import json

with open("./build/manifest.json") as fp:
    preferences = json.load(fp)


filename = sys.argv[0]
sys.argv = [filename, 'build']

include_files = preferences["include_files"]
exclude_files = preferences["exclude_files"]
output_dir = preferences["output_dir"]
icon = preferences["icon"]
name = preferences["name"]
version = preferences["version"]
description = preferences["description"]
main = preferences["main"]
packages = preferences['packages']

os.environ['TCL_LIBRARY'] = preferences["TCL_LIBRARY"]
os.environ['TK_LIBRARY'] = preferences["TK_LIBRARY"]

try:
    shutil.rmtree(preferences["output_dir"])
except FileNotFoundError:
    pass

executables = [Executable(main, icon=icon)]

options = {
    'build_exe': {
        'packages': packages,
        'build_exe': output_dir,
        'include_files': include_files,
    }
}

setup(
    name=name,
    options=options,
    version=version,
    description=description,
    executables=executables
)

for file in exclude_files:
    if os.path.exists(file):
        os.remove(file)
