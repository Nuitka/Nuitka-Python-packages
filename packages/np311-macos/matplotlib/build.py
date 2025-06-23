import __np__
import glob
import shutil
import sys
import os
import sysconfig
import setuptools.build_meta
from tempfile import TemporaryDirectory

import mesonpy

from wheel.wheelfile import WheelFile


def run(wheel_directory):
    __np__.run_with_output("patch", "-t", "-p1", "-i",
                              os.path.join(os.path.dirname(__file__), "matplotlib-static-patch.patch"))

    __np__.patch_all_source(os.getcwd())

    os.environ["MACOSX_DEPLOYMENT_TARGET"] = "10.9"
    os.environ["CMAKE_PREFIX_PATH"] = __np__.find_dep_root("freetype")
    os.environ["INCLUDE"] = sysconfig.get_config_var("INCLUDEPY")
    os.environ["CFLAGS"] = "-I" + sysconfig.get_config_var("INCLUDEPY")
    os.environ["CXXFLAGS"] = "-I" + sysconfig.get_config_var("INCLUDEPY")
    os.environ["PATH"] = (os.path.dirname(__np__.find_build_tool_exe("cmake", "cmake")) + os.pathsep +
                   os.path.dirname(__np__.find_build_tool_exe("ninja", "ninja")) + os.pathsep + os.environ["PATH"])

    __np__.run_with_output(sys.executable, "-m", "build", "-w", "--no-isolation",
                           "-Csetup-args=-Dsystem-freetype=True")

    wheel_location = glob.glob(os.path.join("dist", "matplotlib-*.whl"))[0]

    wheel_files = []
    with TemporaryDirectory() as tmpdir:
        with WheelFile(wheel_location) as wf:
            for filename in wf.namelist():
                wheel_files.append(filename)
                wf.extract(filename, tmpdir)
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "matplotlib/_c_internal_utils.nuitkapython-311-darwin.a"), "matplotlib__c_internal_utils_", [".*fflush.*"])
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "matplotlib/_image.nuitkapython-311-darwin.a"), "matplotlib__image_", [".*fflush.*"])
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "matplotlib/_path.nuitkapython-311-darwin.a"), "matplotlib__path_", [".*fflush.*"])
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "matplotlib/_qhull.nuitkapython-311-darwin.a"), "matplotlib__qhull_", [".*fflush.*"])
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "matplotlib/_tri.nuitkapython-311-darwin.a"), "matplotlib__tri_", [".*fflush.*"])
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "matplotlib/ft2font.nuitkapython-311-darwin.a"), "matplotlib_ft2font_", [".*fflush.*"])
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "matplotlib/backends/_backend_agg.nuitkapython-311-darwin.a"), "matplotlib__backend_agg_", [".*fflush.*"])
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "matplotlib/backends/_tkagg.nuitkapython-311-darwin.a"), "matplotlib__tkagg_", [".*fflush.*"])
        with WheelFile(wheel_location, 'w') as wf:
            for filename in wheel_files:
                wf.write(os.path.join(tmpdir, filename), filename)

    wheel_name = os.path.basename(wheel_location)
    shutil.copy(wheel_location, os.path.join(wheel_directory, wheel_name))
    return os.path.join(wheel_directory, wheel_name)
