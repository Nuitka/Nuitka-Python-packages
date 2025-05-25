import __np__
import glob
import shutil
import sys
import os
import setuptools.build_meta
from tempfile import TemporaryDirectory

import mesonpy

from wheel.wheelfile import WheelFile


def run(wheel_directory):
    __np__.setup_compiler_env()

    __np__.run_build_tool_exe("patch", "patch.exe", "-t", "-p1", "-i",
                              os.path.join(os.path.dirname(__file__), "matplotlib-static-patch.patch"))

    os.environ["CMAKE_PREFIX_PATH"] = __np__.find_dep_root("freetype")

    __np__.run_with_output(sys.executable, "-m", "build", "-w", "--no-isolation",
                           "-Csetup-args=-Dsystem-freetype=True", "-Csetup-args=-Dbuildtype=debug")

    wheel_location = glob.glob(os.path.join("dist", "matplotlib-*.whl"))[0]

    os.environ["PATH"] = (os.path.dirname(__np__.find_build_tool_exe("7zip", "7z.exe")) + os.path.pathsep +
                   os.path.dirname(__np__.find_build_tool_exe("mingw", "objdump.exe")) + os.path.pathsep + os.environ["PATH"])
    wheel_files = []
    with TemporaryDirectory() as tmpdir:
        with WheelFile(wheel_location) as wf:
            for filename in wf.namelist():
                wheel_files.append(filename)
                wf.extract(filename, tmpdir)
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "matplotlib\\_c_internal_utils.lib"), "matplotlib__c_internal_utils_", [".*fflush.*"])
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "matplotlib\\_image.lib"), "matplotlib__image_", [".*fflush.*"])
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "matplotlib\\_path.lib"), "matplotlib__path_", [".*fflush.*"])
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "matplotlib\\_qhull.lib"), "matplotlib__qhull_", [".*fflush.*"])
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "matplotlib\\_tri.lib"), "matplotlib__tri_", [".*fflush.*"])
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "matplotlib\\ft2font.lib"), "matplotlib_ft2font_", [".*fflush.*"])
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "matplotlib\\backends\\_backend_agg.lib"), "matplotlib__backend_agg_", [".*fflush.*"])
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "matplotlib\\backends\\_tkagg.lib"), "matplotlib__tkagg_", [".*fflush.*"])
        with WheelFile(wheel_location, 'w') as wf:
            for filename in wheel_files:
                wf.write(os.path.join(tmpdir, filename), filename)

    wheel_name = os.path.basename(wheel_location)
    shutil.copy(wheel_location, os.path.join(wheel_directory, wheel_name))
    return os.path.join(wheel_directory, wheel_name)
